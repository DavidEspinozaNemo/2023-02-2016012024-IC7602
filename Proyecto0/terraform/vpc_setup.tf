#Main VPC
resource "aws_vpc" "main_vpc" {
  cidr_block           = "192.168.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "Main VPC"
  }
}

#Public subnet
resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.main_vpc.id
  cidr_block              = "192.168.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1a"

  tags = {
    Name = "public-subnet"
  }
}

#Private subnet
resource "aws_subnet" "private_subnet" {
  vpc_id            = aws_vpc.main_vpc.id
  cidr_block        = "192.168.0.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "private-subnet"
  }
}

#Internet gateway for the public subnet
resource "aws_internet_gateway" "main_internet_gw" {
  vpc_id = aws_vpc.main_vpc.id
}

resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.main_vpc.id
}

resource "aws_route" "default_route" {
  route_table_id         = aws_route_table.public_route_table.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.main_internet_gw.id
}

resource "aws_route_table_association" "public_subnet_association" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_route_table.id
}

#NAT gateway to the private subnet
resource "aws_eip" "nat_eip" {
  domain   = "vpc"
}
resource "aws_nat_gateway" "nat" {
  connectivity_type = "private"
  subnet_id         = aws_subnet.private_subnet.id
  allocation_id     = aws_eip.nat_eip.id
}

#Security group
resource "aws_security_group" "securty_group" {
  name        = "main_security_group"
  description = "main security group"
  vpc_id      = aws_vpc.main_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.main_vpc.cidr_block]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.main_vpc.cidr_block]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.main_vpc.cidr_block]
  }

  ingress {
    from_port   = 560
    to_port     = 560
    protocol    = "udp"
    cidr_blocks = [aws_vpc.main_vpc.cidr_block]
  }

  ingress {
    from_port   = 10000
    to_port     = 20000
    protocol    = "udp-tcp"
    cidr_blocks = [aws_vpc.main_vpc.cidr_block]
  }

  ingress {
    from_port   = 4569
    to_port     = 4569
    protocol    = "udp"
    cidr_blocks = [aws_vpc.main_vpc.cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

#Create key pair to access via ssh later
resource "aws_key_pair" "main_auth" {
  key_name   = "mainkey"
  public_key = file("~/.ssh/mainkey.pub")
}
#Create EC2 instances in public subnet
resource "aws_instance" "public_instance" {
  instance_type          = "t3.micro"
  ami                    = data.aws_ami.main_ami.id
  key_name               = aws_key_pair.main_auth.id
  vpc_security_group_ids = [aws_security_group.securty_group.id]
  subnet_id              = aws_subnet.public_subnet.id

}

#Create EC2 instances in private subnet
resource "aws_instance" "private_instance" {
  instance_type          = "t3.micro"
  ami                    = data.aws_ami.main_ami.id
  key_name               = aws_key_pair.main_auth.id
  vpc_security_group_ids = [aws_security_group.securty_group.id]
  subnet_id              = aws_subnet.private_subnet.id

}
