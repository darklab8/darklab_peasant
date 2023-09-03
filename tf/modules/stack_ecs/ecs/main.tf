resource "aws_ecs_cluster" "ecs_cluster" {
  name = var.environment
}
resource "aws_ecs_capacity_provider" "provider" {
  name = "production"
  auto_scaling_group_provider {
    auto_scaling_group_arn         = aws_autoscaling_group.asg.arn
    managed_termination_protection = "DISABLED"

    managed_scaling {
      status          = "ENABLED"
      target_capacity = 100
    }
  }
}

resource "aws_ecs_cluster_capacity_providers" "providers" {
  cluster_name       = aws_ecs_cluster.ecs_cluster.name
  capacity_providers = [aws_ecs_capacity_provider.provider.name]
  default_capacity_provider_strategy {
    base              = 1
    weight            = 100
    capacity_provider = aws_ecs_capacity_provider.provider.name
  }

  lifecycle {
    replace_triggered_by = [
      aws_ecs_capacity_provider.provider.id,
    ]
  }
}