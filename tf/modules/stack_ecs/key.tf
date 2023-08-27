resource "tls_private_key" "example" {
  algorithm = "RSA"
  rsa_bits  = "4096"
}

resource "aws_key_pair" "bastion_key" {
  key_name   = "${var.environment}-bastion"
  public_key = tls_private_key.example.public_key_openssh
}
