resource "tls_private_key" "example" {
  algorithm = "RSA"
  rsa_bits  = "4096"
}

resource "aws_key_pair" "bastion_key" {
  key_name   = "${var.environment}-bastion"
  public_key = tls_private_key.example.public_key_openssh
}

resource "aws_security_group" "bastion_host" {
  name        = "${var.environment}_SecurityGroup_BastionHost"
  description = "Bastion host Security Group"
  vpc_id      = var.network.vpc.id

  ingress {
    description = "Allow SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] ## The IP range could be limited to the developers IP addresses if they are fix
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }
}

data "aws_ami" "amazon_linux_2" {
  most_recent = true

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "owner-alias"
    values = ["amazon"]
  }

  filter {
    name   = "name"
    values = ["amzn2-ami-ecs-hvm-*-x86_64-ebs"]
  }

  owners = ["amazon"]
}

resource "aws_instance" "bastion_host" {
  ami                         = data.aws_ami.amazon_linux_2.id
  instance_type               = "t3.micro"
  subnet_id                   = var.network.pub_subnet.id
  associate_public_ip_address = true
  key_name                    = aws_key_pair.bastion_key.id
  vpc_security_group_ids      = [aws_security_group.bastion_host.id]

  tags = {
    Name     = "${var.environment}_EC2_BastionHost"
  }
}