# instalacion de la instancia OpenVPN
# eso va en el vpc.tf

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

# una vez instalado en la instancia, se deben realizar configuraciones
# Recurso null_resource para copiar el archivo server.conf y reiniciar OpenVPN
resource "null_resource" "configure_openvpn" {
  # Dependencia en la instancia EC2 de OpenVPN para garantizar que se ejecute después de su creación
  depends_on = [aws_instance.openvpn_instance]

  # Provisión de Terraform para copiar el archivo de configuración a la instancia
  provisioner "file" {
    source      = "./server_vpn.conf"           # Ruta local del archivo server.conf
    destination = "/etc/openvpn/server.conf"    # Ruta en la instancia EC2
    connection {
      type        = "ssh"
      user        = "ubuntu"  # Usuario SSH en la instancia (ajústalo según tu caso)
      private_key = file("~/.ssh/your-private-key.pem")  # Ruta a la clave privada SSH
      host        = aws_instance.openvpn_instance.public_ip  # IP pública de la instancia
    }
  }

  # Provisión de Terraform para reiniciar el servicio OpenVPN
  provisioner "remote-exec" {
    inline = [
      "sudo systemctl restart openvpn",  # Comando para reiniciar OpenVPN
    ]
    connection {
      type        = "ssh"
      user        = "ubuntu"  # Usuario SSH en la instancia (ajústalo según tu caso)
      private_key = file("~/.ssh/your-private-key.pem")  # Ruta a la clave privada SSH
      host        = aws_instance.openvpn_instance.public_ip  # IP pública de la instancia
    }
  }
}