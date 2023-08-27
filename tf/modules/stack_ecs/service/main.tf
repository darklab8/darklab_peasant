resource "aws_ecs_task_definition" "service" {
  family                = local.family
  container_definitions = try(nonsensitive(local.container_def), local.container_def)
}

resource "aws_ecs_service" "service" {
  name            = aws_ecs_task_definition.service.family
  cluster         = var.ecs.ecs_cluster.id
  task_definition = aws_ecs_task_definition.service.arn
  desired_count   = 1
  launch_type     = "EC2" 
}

locals {
  family = "${var.environment}-${var.name}-${var.task}"
  container_def = jsonencode([{
    essential   = true
    memory      = 50
    name        = local.family
    cpu         = 1
    image       = "nginx:latest"
    environment = []
  }])
}