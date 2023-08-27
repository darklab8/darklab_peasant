module "network" {
  source = "./network"
}

module "ecs" {
  # generic guide https://docs.aws.amazon.com/AmazonECS/latest/developerguide/get-set-up-for-amazon-ecs.html
  source      = "./ecs"
  network     = module.network
  environment = var.environment
  instance_key   = aws_key_pair.bastion_key.key_name
}

module "redis" {
  source  = "./redis"
  network = module.network
}

module "service_example" {
  source      = "./service"
  name        = "example"
  ecs         = module.ecs
  environment = var.environment
}