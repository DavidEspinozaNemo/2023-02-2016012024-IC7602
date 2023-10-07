# instalacion de la instancia OpenVPN

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