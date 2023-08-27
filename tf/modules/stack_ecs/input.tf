locals {
  name = "peasant"
}

variable "environment" {
  type = string
}

variable "ecr" {
  type = object({
    repository_url = string
  })
}