variable "function" {
  type = object({
    function_name = string
    arn           = string
  })
}

variable "lambda_input" {
  type = string
}

variable "schedule" {
  type = object({
    hours   = number
    minutes = number
  })
}

variable "event_name" {
  type = string
}

resource "aws_cloudwatch_event_rule" "schedule" {
  name                = var.event_name
  schedule_expression = "cron(${var.schedule.minutes} ${var.schedule.hours} * * ? *)"
}

resource "aws_cloudwatch_event_target" "schedule_lambda" {
  rule      = aws_cloudwatch_event_rule.schedule.name
  target_id = var.function.function_name
  arn       = var.function.arn

  input_transformer {
    input_template = var.lambda_input
  }
}
