# not working due to Selenium Chrome not being launchable in AWS lambdas via docker
# /etc/hosts or some other unsolvable at the moment problem
# module "stack_lambda" {
#   source      = "../modules/stack_lambda"
#   environment = "production"
#   ecr = module.ecr
# }
