resource "aws_vpc" "main_vpc" {
  cidr_block = "10.0.0.0/16"
}

#===================Internet gateway===============================
resource "aws_internet_gateway" "main_internet_gw" {
  vpc_id = aws_vpc.main_vpc.id
}

#===================Public route table===============================
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main_vpc.id

  # route {
  #   cidr_block = "0.0.0.0/0"
  #   gateway_id = aws_internet_gateway.main_vpc.id
  # }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

#==================NAT gateway===============================
#todo: NAT here

#===================Public subnet===============================
resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.main_vpc.id
  cidr_block = "10.0.0.0/22"
}

#===================Private subnet===============================
resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.main_vpc.id
  cidr_block = "10.0.4.0/22"
}

#===================Public instance===============================
resource "aws_instance" "public_instance" {
  ami                    = data.aws_ami.main_ami.id
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.allow_traffic.id]
  key_name               = aws_key_pair.main_auth.id

  tags = {
    Name = "Public instance"
  }
}

#===================Private instance===============================
resource "aws_instance" "private_instance" {
  ami                    = data.aws_ami.main_ami.id
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.private.id
  vpc_security_group_ids = [aws_security_group.allow_traffic.id]
  key_name               = aws_key_pair.main_auth.id

  tags = {
    Name = "Private instance"
  }
}

#===================DNS Server (Subred Pública)===============================
resource "aws_instance" "dns_server" {
  ami                    = data.aws_ami.main_ami.id
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.allow_traffic.id]
  key_name               = aws_key_pair.main_auth.key_name

  tags = {
    Name = "DNS Server"
  }
}

#===================Reverse Proxy (Subred Pública)===============================
resource "aws_instance" "reverse_proxy" {
  ami                    = data.aws_ami.main_ami.id
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.allow_traffic.id]
  key_name               = aws_key_pair.main_auth.key_name

  tags = {
    Name = "Reverse Proxy"
  }
}

#===================Web Cache (Subred Pública)===============================
resource "aws_instance" "web_cache" {
  ami                    = data.aws_ami.main_ami.id
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.allow_traffic.id]
  key_name               = aws_key_pair.main_auth.key_name

  tags = {
    Name = "Web Cache"
  }
}

#===================Apache Server 1 (Subred Privada)===============================
resource "aws_instance" "apache_server_1" {
  ami                    = data.aws_ami.main_ami.id
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.private.id
  vpc_security_group_ids = [aws_security_group.allow_traffic.id]
  key_name               = aws_key_pair.main_auth.key_name

  tags = {
    Name = "Apache Server 1"
  }
}

#===================Apache Server 2 (Subred Privada)===============================
resource "aws_instance" "apache_server_2" {
  ami                    = data.aws_ami.main_ami.id
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.private.id
  vpc_security_group_ids = [aws_security_group.allow_traffic.id]
  key_name               = aws_key_pair.main_auth.key_name

  tags = {
    Name = "Apache Server 2"
  }
}

#===================OpenVPN (Subred Publica)===============================
resource "aws_instance" "openvpn_instance" {
  ami           = data.aws_ami.main_ami.id
  instance_type = "t3.micro"               # Tipo de instancia (ajústalo según tus necesidades)
  subnet_id     = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.allow_traffic.id]
  key_name      = aws_key_pair.main_auth.key_name

  tags = {
    Name = "OpenVPN Instance"
  }
}

# Salida para mostrar la IP pública de la instancia
output "instance_public_ip" {
  value       = aws_instance.openvpn_instance.public_ip
  description = "IP pública de la instancia OpenVPN"
}

# Recurso null_resource para ejecutar comandos en la instancia EC2
resource "null_resource" "install_openvpn" {
  # Dependencia en la instancia EC2 para garantizar que se ejecute después de su creación
  depends_on = [aws_instance.openvpn_instance]

  # Configuración de la conexión SSH a la instancia
  connection {
    type        = "ssh"
    user        = "ubuntu"  # Usuario SSH en la instancia (puede variar según la AMI)
    private_key = file("~/.ssh/your-private-key.pem")  # Ruta a la clave privada SSH
    host        = aws_instance.openvpn_instance.public_ip  # IP pública de la instancia
  }

  # Comando a ejecutar en la instancia para instalar OpenVPN desde tu archivo .sh
  provisioner "remote-exec" {
    inline = [
      "chmod +x ./install_openvpn.sh",  # Cambia los permisos del archivo para que sea ejecutable
      "./install_openvpn.sh"            # Ejecuta el script de instalación de OpenVPN
    ]
  }
}

#=================== Security Group===============================
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