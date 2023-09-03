resource "aws_eip" "gateway" {
  vpc        = true
  depends_on = [aws_internet_gateway.gateway]
}

resource "aws_nat_gateway" "gateway" {
  subnet_id     = aws_subnet.public.id
  allocation_id = aws_eip.gateway.id
}

resource "aws_subnet" "private" {
  cidr_block        = "10.0.2.0/24"
  availability_zone = "eu-west-1a"
  vpc_id            = aws_vpc.vpc.id
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.gateway.id
  }
}

resource "aws_route_table_association" "private" {
  subnet_id      = aws_subnet.private.id
  route_table_id = aws_route_table.private.id
}

resource "aws_service_discovery_private_dns_namespace" "ns" {
  name        = "ecs.discovery"
  description = "ecs private discovery namespace"
  vpc         = aws_vpc.vpc.id
}

#  NAT stuff
# Based on stuff from here
# https://www.architect.io/blog/2021-03-30/create-and-manage-an-aws-ecs-cluster-with-terraform/
# resource "aws_route" "internet_access" {
#   route_table_id         = aws_vpc.vpc.main_route_table_id
#   destination_cidr_block = "0.0.0.0/0"

#   gateway_id             = aws_internet_gateway.gateway.id
# }

