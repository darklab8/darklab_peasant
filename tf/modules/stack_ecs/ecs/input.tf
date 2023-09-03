variable "network" {
  type = object({
    ecs_sg = object({
      id = string
    })
    pub_subnet = object({
      id = string
    })
    private_subnet = object({
      id = string
    })    
  })
}

variable "environment" {
  type = string
}

variable "instance_key" {}
