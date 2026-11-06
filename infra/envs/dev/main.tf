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

module "frontend" {
  source = "../../modules/frontend"
  name   = "urlshort"
  env    = "dev"
}

module "api" {
  source            = "../../modules/api"
  name              = local.name
  lambda_invoke_arn = module.lambda.invoke_arn
  lambda_name       = module.lambda.function_name
  allowed_origins   = ["https://${module.frontend.domain}"]
}

output "api_url" { value = module.api.api_url }
output "web_bucket" { value = module.frontend.bucket }
output "distribution_id" { value = module.frontend.distribution_id }
output "web_url" { value = "https://${module.frontend.domain}" }
