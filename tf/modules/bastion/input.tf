variable environment {
    type = string
}

output "key_name" {
    value = aws_key_pair.bastion_key.key_name
}

output "bastion_private_key" {
    value = tls_private_key.example.private_key_openssh
    sensitive = true
}

variable "network" {
  type = object({
    vpc = object({
      id = string
    })
    pub_subnet = object({
      id = string
    })
  })
}
