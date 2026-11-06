variable "name" { type = string }

resource "aws_dynamodb_table" "this" {
  name         = var.name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "shortId"

  attribute {
    name = "shortId"
    type = "S"
  }

  ttl {
    attribute_name = "expires_at"
    enabled        = true
  }
}

output "name" { value = aws_dynamodb_table.this.name }
output "arn" { value = aws_dynamodb_table.this.arn }
