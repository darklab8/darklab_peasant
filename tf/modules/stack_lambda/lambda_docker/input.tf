variable "module_path" {
  type = string
}

variable "environment" {
  type        = string
  description = "staging / production"
}

variable "timeout" {
  type    = number
  default = null
}

locals {
  timeout1 = var.environment == "production" ? 60 * 10 : 10
  timeout  = var.timeout != null ? var.timeout : local.timeout1
}

variable "lambda_role_arn" {
  type = string
}

variable "lambda_name" {
  type = string
}

variable "description" {
  type = string
}
variable "memory_size" {
  type    = number
  default = null
}

variable "image_tag" {
  type = string
}

variable "repository_url" {
  type = string
}