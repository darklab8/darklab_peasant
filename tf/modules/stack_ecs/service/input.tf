variable "environment" {
  type = string
}

variable "name" {
  type = string
}

variable "task" {
  type    = string
  default = "app"
}

variable "ecs" {
  type = object({
    ecs_cluster = object({
      id = string
    })
  })
}