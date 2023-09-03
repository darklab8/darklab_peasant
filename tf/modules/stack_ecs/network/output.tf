output "ecs_sg" {
  value = aws_security_group.ecs_sg
}

output "redis_sg" {
  value = aws_security_group.redis_sg
}

output "pub_subnet" {
  value = aws_subnet.public
}

output "private_subnet" {
  value = aws_subnet.private
}

output "vpc" {
  value = aws_vpc.vpc
}
