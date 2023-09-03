# module "stack_ecs" {
#   source      = "../modules/stack_ecs"
#   environment = "production"
#   ecr         = module.ecr
# }
# output "bastion_private_key" {
#     value = module.stack_ecs.bastion_private_key
#     sensitive = true
# }
