module "ecr" {
  source = "../ecr"
  name   = local.name
}

module "lambda" {
  source          = "../lambda_docker"
  environment     = var.environment
  module_path     = path.module
  lambda_name     = local.name
  lambda_role_arn = module.role.arn
  description     = "Creates health check for document submitting"
  timeout         = 60 * 2 # 2 minutes
  image_tag       = local.image_tag
  repository_url  = module.ecr.repository_url
}

locals {
  image_tag = "0.0.0"
  lambda_input = {

  }
}

resource "aws_lambda_invocation" "first_init" {
  function_name = module.lambda.function_name
  input         = jsonencode(local.lambda_input)
}

locals {
  schedules = [
    {
      hours   = 10
      minutes = 0
    }
  ]
}

module "schedule" {
  count        = length(local.schedules)
  source       = "../lambda_schedule"
  function     = module.lambda.function
  lambda_input = jsonencode(local.lambda_input)
  schedule     = local.schedules[count.index]
  event_name   = "${module.lambda.function.function_name}-schedule-${count.index}"
}
