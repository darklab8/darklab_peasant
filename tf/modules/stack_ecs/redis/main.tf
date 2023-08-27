variable "network" {
  type = object({
    pub_subnet = object({
      id = string
    })
    pub_subnet2 = object({
      id = string
    })
    redis_sg = object({
      id = string
    })
    ecs_sg = object({
      id = string
    })
  })
}

resource "aws_elasticache_subnet_group" "main" {
  name       = "my-cache-subnet"
  subnet_ids = [var.network.pub_subnet.id, var.network.pub_subnet2.id]
}

resource "aws_elasticache_cluster" "main" {
  cluster_id           = "peasant"
  engine               = "redis"
  node_type            = "cache.t2.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis3.2"
  engine_version       = "3.2.10"
  port                 = 6379
  subnet_group_name    = aws_elasticache_subnet_group.main.name
  security_group_ids   = [var.network.redis_sg.id, var.network.ecs_sg.id]
}

