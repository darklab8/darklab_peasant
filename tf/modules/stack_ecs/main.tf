module "network" {
  source = "./network"
  environment = var.environment
  vpc_cidr_block = "10.0.0.0/16"
}

module "ecs" {
  # generic guide https://docs.aws.amazon.com/AmazonECS/latest/developerguide/get-set-up-for-amazon-ecs.html
  source      = "./ecs"
  network     = module.network
  environment = var.environment
  instance_key   = module.bastion.key_name
}

module "bastion" {
  source  = "../bastion"
  environment = var.environment
  network = module.network
}
output "bastion_private_key" {
    value = module.bastion.bastion_private_key
    sensitive = true
}

# module "redis" {
#   source  = "./redis"
#   network = module.network
# }

module "service_example" {
  source      = "./service"
  name        = "example"
  ecs         = module.ecs
  environment = var.environment
}