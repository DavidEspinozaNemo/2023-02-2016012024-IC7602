# Conéctate a la instancia EC2
ssh -i <ruta_a_tu_clave_privada> ubuntu@<dirección_IP_pública_de_la_instancia>

# Actualiza el sistema
sudo apt-get update

# Instala OpenVPN
sudo apt-get install openvpn -y