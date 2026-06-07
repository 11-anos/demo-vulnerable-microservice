terraform {
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

resource "aws_security_group" "app_sg" {
  name        = "analytics-app-sg"
  description = "Security group for analytics service"
  vpc_id      = var.vpc_id

  # Allow HTTPS from LB
  ingress {
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [var.alb_sg_id]
  }

  # TODO: restrict this before prod — needed for ops team SSH access now
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

variable "vpc_id" {}
variable "alb_sg_id" {}
