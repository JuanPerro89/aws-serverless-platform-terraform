provider "aws" { region = "eu-west-1" }

locals { name = "urlshort-dev" }

module "dynamodb" {
  source = "../../modules/dynamodb"
  name   = local.name
}

module "lambda" {
  source     = "../../modules/lambda"
  name       = local.name
  source_dir = "${path.root}/../../../app/src"
  table_name = module.dynamodb.name
  table_arn  = module.dynamodb.arn
}

module "api" {
  source            = "../../modules/api"
  name              = local.name
  lambda_invoke_arn = module.lambda.invoke_arn
  lambda_name       = module.lambda.function_name
}

output "api_url" { value = module.api.api_url }