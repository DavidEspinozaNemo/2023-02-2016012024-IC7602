# Configura el proveedor de AWS
provider "aws" {
  region  = "us-east-1"  # Cambia la región según tu preferencia
  profile = "dev"        # Cambia el perfil si es necesario
}

# Define una variable para el nombre de la instancia
variable "instance_name" {
  description = "Inst. OpenVPN"
  default     = "openvpn-instance"
}

# Crea una instancia EC2
resource "aws_instance" "openvpn_instance" {
  ami           = "ami-007a18d38016a0f4e"  # AMI de Ubuntu (puedes cambiarla)
  instance_type = "t3.micro"               # Tipo de instancia (ajústalo según tus necesidades)
  tags = {
    Name = var.instance_name
  }
  # Aquí puedes agregar más configuraciones como grupos de seguridad, subred, etc.
  # ...
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

# Definir reglas de firewall
# El recurso "aws_security_group" para definir reglas de seguridad.
resource "aws_security_group" "openvpn_security_group" {
  name        = "openvpn-security-group"
  description = "Reglas de seguridad para OpenVPN"
  vpc_id      = aws_instance.openvpn_instance.vpc_security_group_ids[0]  # Obtén el ID del grupo de seguridad de la instancia
}

# Agrupamos varias reglas en un solo recurso aws_security_group_rule
resource "aws_security_group_rule" "openvpn_rules" {
  type        = "ingress"
  security_group_id = aws_security_group.openvpn_security_group.id

  rule {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["192.168.1.0/24"]
  }

  rule {
    from_port   = 1194
    to_port     = 1194
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Puedes seguir agregando más reglas aquí según tus necesidades
}