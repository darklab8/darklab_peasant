output "arn" {
  value       = aws_iam_role.role.arn
  description = "The ARN of the generated role"
}
output "name" {
  description = "The name of the role"
  value       = aws_iam_role.role.name
}
