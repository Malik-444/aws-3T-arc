# making the alb
  load_balancer_typer = resource "aws_lb" "3tier-alb" {
  name               = "3tier-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb_sg.id]
  subnets            = [for subnet in aws_subnet.public : subnet.id]

#target group 

resource "aws_lb_target_group" "test" {
  name     = "for-ec2"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

 

  tags = {
    Environment = "3tier-alb"
  }
}
