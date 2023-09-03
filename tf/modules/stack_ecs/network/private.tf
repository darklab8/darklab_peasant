resource "aws_subnet" "private" {
  cidr_block        = "10.0.2.0/24"
  availability_zone = "eu-west-1a"
  vpc_id            = aws_vpc.vpc.id
  map_public_ip_on_launch = false
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.vpc.id
}

resource "aws_route" "default_route" {
  route_table_id         = aws_route_table.private.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.gateway.id
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

## extra

resource "aws_eip" "eip_nat_gateways" {
  vpc        = true
}

resource "aws_nat_gateway" "gateway" {
  subnet_id     = aws_subnet.public.id
  allocation_id = aws_eip.eip_nat_gateways.id
}

#  NAT stuff
# Based on stuff from here
# https://www.architect.io/blog/2021-03-30/create-and-manage-an-aws-ecs-cluster-with-terraform/
# resource "aws_route" "internet_access" {
#   route_table_id         = aws_vpc.vpc.main_route_table_id
#   destination_cidr_block = "0.0.0.0/0"

#   gateway_id             = aws_internet_gateway.gateway.id
# }

