# Creación de una VPC en AWS
resource "aws_vpc" "main_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "Main VPC"
  }
}

#===================Internet gateway===============================
# Creación de un Internet Gateway para habilitar la conectividad a Internet
resource "aws_internet_gateway" "main_internet_gw" {
  vpc_id = aws_vpc.main_vpc.id
}

#===================Public subnet===============================
# Creación de una subred pública en la VPC
resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.main_vpc.id
  cidr_block = "10.0.0.0/22"
  map_public_ip_on_launch = true
}

#===================Private subnet===============================
# Creación de una subred privada en la VPC
resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main_vpc.id
  cidr_block = "10.0.4.0/22"
}

#===================Public route table===============================
# Creación de una tabla de rutas pública para la VPC
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main_vpc.id

  # Comentar o descomentar la sección de rutas según sea necesario
  # para permitir o restringir el tráfico hacia Internet.
  # Por defecto, no tiene rutas configuradas.

  # route {
  #   cidr_block = "0.0.0.0/0"
  #   gateway_id = aws_internet_gateway.main_vpc.id
  # }
}

# Asociación de la tabla de rutas pública con una subred pública
resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route" "default_route" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.main_internet_gw.id
}

#==================NAT gateway===============================
# Creación de una Elastic IP (EIP) para el NAT Gateway
# Nat resource
resource "aws_eip" "nat" {
  domain = "vpc"
}

# Creación de un NAT Gateway para permitir que las instancias en la VPC accedan a Internet
resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public.id
}

# Creación de una tabla de rutas privada para la VPC
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main_vpc.id
}

# Configuración de una ruta en la tabla de rutas privada que apunte al NAT Gateway
resource "aws_route" "private_nat" {
  route_table_id         = aws_route_table.private.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.main.id
}

# Asociación de la tabla de rutas privada con una subred privada
resource "aws_route_table_association" "private" {
  subnet_id      = aws_subnet.private.id
  route_table_id = aws_route_table.private.id
}

resource "aws_instance" "vpn_server" {
  ami                    = data.aws_ami.main_ami.id
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.allow_traffic.id]
  key_name               = aws_key_pair.main_auth.key_name

  tags = {
    Name = "VPN Server"
  }
}
resource "aws_instance" "bastion_host" {
  ami                    = data.aws_ami.main_ami.id
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.allow_traffic.id]
  key_name               = aws_key_pair.main_auth.key_name

  tags = {
    Name = "Bastion host"
  }
}

#===================DNS Server (Subred Pública)===============================
# Creación de una instancia para un servidor DNS en una subred pública
resource "aws_instance" "dns_server" {
  ami                    = data.aws_ami.main_ami.id
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.allow_traffic.id]
  key_name               = aws_key_pair.main_auth.key_name

  tags = {
    Name = "DNS Server"
  }
}

#===================Reverse Proxy (Subred Pública)===============================
# Creación de una instancia para un servidor Reverse Proxy en una subred públicar
resource "aws_instance" "reverse_proxy" {
  ami                    = data.aws_ami.main_ami.id
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.allow_traffic.id]
  key_name               = aws_key_pair.main_auth.key_name

  tags = {
    Name = "Reverse Proxy"
  }
}

#===================Web Cache (Subred Pública)===============================
# Creación de una instancia para un servidor Web Cache en una subred pública
resource "aws_instance" "web_cache" {
  ami                    = data.aws_ami.main_ami.id
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.allow_traffic.id]
  key_name               = aws_key_pair.main_auth.key_name

  tags = {
    Name = "Web Cache"
  }
}

#===================Apache Server 1 (Subred Privada)===============================
#  Creación de una instancia para un servidor Apache en una subred privada
resource "aws_instance" "apache_server_1" {
  ami                    = data.aws_ami.main_ami.id
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.private.id
  vpc_security_group_ids = [aws_security_group.allow_traffic.id]
  key_name               = aws_key_pair.main_auth.key_name

  tags = {
    Name = "Apache Server 1"
  }
}

#===================Apache Server 2 (Subred Privada)===============================
# Creación de otra instancia para un servidor Apache en una subred privada
resource "aws_instance" "apache_server_2" {
  ami                    = data.aws_ami.main_ami.id
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.private.id
  vpc_security_group_ids = [aws_security_group.allow_traffic.id]
  key_name               = aws_key_pair.main_auth.key_name

  tags = {
    Name = "Apache Server 2"
  }
}

#=================== Security Group===============================
# Creación de un grupo de seguridad para permitir el tráfico necesario
resource "aws_security_group" "allow_traffic" {
  name        = "p1_security_group"
  description = "p1 security group"
  vpc_id      = aws_vpc.main_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 3128
    to_port     = 3128
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = -1
    to_port     = -1
    protocol    = "icmp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 53
    to_port     = 53
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] 
  }

  ingress {
    from_port   = 53
    to_port     = 53
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"] 
  }
  ingress {
    from_port   = 1194
    to_port     = 1194
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"] 
  }


  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

#Create key pair to access via ssh later
# Creación de un par de claves para acceder a las instancias a través de SSH
resource "aws_key_pair" "main_auth" {
  key_name   = "mainkey"
  public_key = file("~/.ssh/mainkey.pub")
}