module "lambda" {
  source          = "./lambda_docker"
  environment     = var.environment
  module_path     = path.module
  lambda_name     = local.name
  lambda_role_arn = module.role.arn
  description     = "Creates health check for document submitting"
  timeout         = 60 * 2 # 2 minutes
  image_tag       = local.image_tag
  repository_url  = var.ecr.repository_url
  memory_size     = 3008
}

data "aws_ssm_parameter" "config" {
  name = "/terraform/${var.environment}/pesant"
}

locals {
  image_tag    = "0.11"
  lambda_input = jsondecode(data.aws_ssm_parameter.config.value)
}

resource "aws_lambda_invocation" "first_init" {
  function_name = module.lambda.function_name
  input         = jsonencode(merge(local.lambda_input, { test_mode = false }))
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
