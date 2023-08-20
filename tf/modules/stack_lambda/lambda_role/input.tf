variable "name" {
  type        = string
  description = "name of the role. Should be unique by account"
}

variable "path" {
  type        = string
  default     = "/"
  description = "A folder to sort IAM roles"
}

variable "tags" {
  type        = map(string)
  description = "Additional tags on the lambda"
  default     = {}
}
