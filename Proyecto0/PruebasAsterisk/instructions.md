*) actualizar todos los paquetes a la última versión

apt-get update -y
apt-get upgrade -y

*) instalar algunas dependencias necesarias para FreePBX

apt-get install unzip git gnupg2 curl libnewt-dev libssl-dev libncurses5-dev subversion libsqlite3-dev build-essential libjansson-dev libxml2-dev uuid-dev subversion -y

*) FreePBX requiere un Asterisk para estar instalado en su servidor
*) descargar la última versión de Asterisk 

wget http://downloads.asterisk.org/pub/telephony/asterisk/asterisk-18-current.tar.gz

*) extraer el archivo descargado

tar -xvzf asterisk-18-current.tar.gz

*) ejecute el siguiente script para instalar todas las dependencias necesarias:

cd asterisk-18.*
contrib/scripts/get_mp3_source.sh
contrib/scripts/install_prereq install

*) ir al menu de configuracion:

./configure

*) Se debe ver asi:

configure: Menuselect build configuration successfully completed
...
configure: Package configured for:
configure: OS type  : linux-gnu
configure: Host CPU : x86_64
configure: build-cpu:vendor:os: x86_64 : pc : linux-gnu :
configure: host-cpu:vendor:os: x86_64 : pc : linux-gnu :

*) para seleccionar módulos y complementos de Asterisk, ejecutar el siguiente comando:

make menuselect

*) Se seleccionan atravez de una interfaz, navegar con el teclado y el raton:
*) Habilitar:

Add-ons:
- chan_mobile
- chan_ooh323
- format_mp3
- res_config_msql

Modulos de sonidos centrales

Core Sounds Packages:
- CORE-SOUNDS-EN-WAV
- CORE-SOUNDS-EN-ULAM
- CORE-SOUNDS-EN-GSM
- CORE-SOUNDS-EN-G729
- CORE-SOUNDS-EN-G722
- CORE-SOUNDS-EN-SLN16
- CORE-SOUNDS-EN-SIREN7
- CORE-SOUNDS-EN-SIREN14

Modulos de musica de espera

Music On Hold File Package:
- MOH-OPSOUND-WAV
- MOH-OPSOUND-ULAM
- MOH-OPSOUND-ALAM
- MOH-OPSOUND-GSM

Modulos de sonidos extra:

Extra Sounds Package:
- EXTRA-SOUNDS-EN-WAV
- EXTRA-SOUNDS-EN-ULAM
- EXTRA-SOUNDS-EN-ALAM
- EXTRA-SOUNDS-EN-GSM
- EXTRA-SOUNDS-EN-G729
- EXTRA-SOUNDS-EN-G722
- EXTRA-SOUNDS-EN-SLN16
- EXTRA-SOUNDS-EN-SIREN7

*) Después de seleccionar todos los componentes necesarios, hacer clic en el botón Guardar y salir para cerrar la consola.
*) Ejecutar el siguiente comando para compilar el asterisco:

make -j2

*)  instale Asterisk

make install

*) ejecutar los siguientes comandos para instalar ejemplos y configurar:

make samples
make config
ldconfig
