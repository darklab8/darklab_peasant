output "ecs_sg" {
  value = aws_security_group.ecs_sg
}

output "redis_sg" {
  value = aws_security_group.redis_sg
}

output "pub_subnet" {
  value = aws_subnet.pub_subnet
}

output "pub_subnet2" {
  value = aws_subnet.pub_subnet2
}