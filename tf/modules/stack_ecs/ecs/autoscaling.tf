locals {
  user_data = templatefile("${path.module}/join_ecs.sh", {
    cluster = aws_ecs_cluster.ecs_cluster.name
  })
}

resource "aws_launch_configuration" "ecs_launch_config" {
  # found here https://aws.amazon.com/marketplace/pp/prodview-do6i4ripwbhs2
  image_id             = "ami-0c5cd894db560d66c" # free tier ECS optimized
  iam_instance_profile = aws_iam_instance_profile.ecs_agent.name
  security_groups      = [var.network.ecs_sg.id]
  user_data            = local.user_data
  instance_type        = "t2.micro"

  key_name                    = var.instance_key
}

resource "aws_autoscaling_group" "failure_analysis_ecs_asg" {
  name                 = "asg"
  vpc_zone_identifier  = [var.network.pub_subnet.id]
  launch_configuration = aws_launch_configuration.ecs_launch_config.name

  desired_capacity          = 1
  min_size                  = 1
  max_size                  = 1
  health_check_grace_period = 300
  health_check_type         = "EC2"

  depends_on = [
    aws_launch_configuration.ecs_launch_config
  ]

  lifecycle {
    replace_triggered_by = [
     aws_launch_configuration.ecs_launch_config.id,
    ]
  }
}
