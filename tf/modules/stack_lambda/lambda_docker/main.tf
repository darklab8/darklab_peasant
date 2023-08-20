resource "aws_lambda_function" "main" {
  function_name = var.lambda_name
  role          = var.lambda_role_arn
  description   = var.description
  timeout       = local.timeout
  memory_size   = var.memory_size
  package_type  = "Image"
  image_uri     = "${var.repository_url}:${var.image_tag}"
}
