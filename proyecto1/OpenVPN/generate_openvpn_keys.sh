#!/bin/bash

# Variables de configuración
export KEY_COUNTRY="US"
export KEY_PROVINCE="CA"
export KEY_CITY="SanFrancisco"
export KEY_ORG="MyCompany"
export KEY_EMAIL="admin@mycompany.com"
export KEY_OU="MyOrgUnit"

# Directorio de trabajo para easy-rsa
EASY_RSA_DIR="/etc/openvpn/easy-rsa"

# Cambiar al directorio de easy-rsa
cd $EASY_RSA_DIR

# Limpia cualquier configuración anterior
./clean-all

# Genera el certificado de autoridad de certificación (CA)
./build-ca

# Genera el certificado y la clave del servidor
./build-key-server server

# Genera el archivo Diffie-Hellman
./build-dh

# Copia los archivos generados a la ubicación correcta
cp $EASY_RSA_DIR/keys/{ca.crt,server.crt,server.key,dh2048.pem} /etc/openvpn/

# Reinicia el servicio OpenVPN
systemctl restart openvpn

# Limpia el entorno
unset KEY_COUNTRY
unset KEY_PROVINCE
unset KEY_CITY
unset KEY_ORG
unset KEY_EMAIL
unset KEY_OU

# Finaliza la generación de claves
exit 0
