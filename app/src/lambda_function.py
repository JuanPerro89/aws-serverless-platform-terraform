import json
import os
import time
import boto3
import string
import secrets
from urllib.parse import urlparse

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])  # CAMBIO: antes 'url-shortener'

MAX_URL_LENGTH = 2048
TTL_SECONDS = 180 * 24 * 3600  # CAMBIO: caducidad a 6 meses


def generate_short_id(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


def is_valid_url(url):
    if not isinstance(url, str) or len(url) > MAX_URL_LENGTH:
        return False
    try:
        parsed = urlparse(url)
    except ValueError:
        return False
    return parsed.scheme in ('http', 'https') and bool(parsed.netloc)


def lambda_handler(event, context):
    method = event['requestContext']['http']['method']
    path = event['rawPath']

    if method == 'GET' and path != '/':
        short_id = path.strip('/')
        response = table.get_item(Key={'shortId': short_id})

        if 'Item' in response:
            return {
                'statusCode': 301,
                'headers': {'Location': response['Item']['longUrl']}
            }
        return {'statusCode': 404, 'body': json.dumps('URL no encontrada')}

    elif method == 'POST':
        try:
            body = json.loads(event.get('body', '{}'))
        except json.JSONDecodeError:
            return {'statusCode': 400, 'body': json.dumps('JSON invalido')}
        long_url = body.get('url')

        if not is_valid_url(long_url):
            return {'statusCode': 400, 'body': json.dumps('URL invalida')}

        short_id = generate_short_id()
        try:
            table.put_item(
                Item={
                    'shortId': short_id,
                    'longUrl': long_url,
                    'expires_at': int(time.time()) + TTL_SECONDS,  # CAMBIO
                },
                ConditionExpression='attribute_not_exists(shortId)'
            )
        except table.meta.client.exceptions.ConditionalCheckFailedException:
            return {'statusCode': 409, 'body': json.dumps('ID repetido, reintenta')}

        host = event['headers'].get('host', '')
        shortened_url = f"https://{host}/{short_id}"

        return {
            'statusCode': 200,
            'body': json.dumps({'shortUrl': shortened_url})
        }

    return {'statusCode': 400, 'body': 'Peticion incorrecta'}