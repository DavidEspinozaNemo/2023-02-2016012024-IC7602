xximagenxx

**Escuela de Ingeniería en Computación **

**Proyecto opcional** 

**Redes** 

Profesor: Gerardo Nereo Campos Araya

Estudiantes:

Ángel Villalobos Peña   - 2014015712

Sebastián Díaz Obando  - 2020041942

Fernando Alvarez Olsen  - 2019171657

Tania María Sánchez Irola - 2018138723

David Jose Espinoza Soto - 2016012024


Fecha de entrega: Martes 22 de agosto del 2023



# Introducción

​	En los tiempos actuales la automatización  y la gestión eficiente son fundamentales. Este proyecto implementa tecnologías de automatización de infraestructura y administración de configuración. 
​	El presente trabajo se enfoca en la creación y configuración de una red virtual funcional que consta de dos subredes. Se establece una red pública, accesible desde Internet, y una red privada, que permite acceso a Internet, pero no es accesible directamente desde la red global. Para garantizar la seguridad y el control del tráfico, se implementará un dispositivo de Traducción de Direcciones de Red (NAT) en la red privada.
​	La implementación de la infraestructura se lleva a cabo utilizando la herramienta Terraform, que permite definir y desplegar la infraestructura como código (IaC). Aunque el proyecto hace uso de Amazon Web Services (AWS). El proyecto se sumerge en la instalación automatizada de las tecnologías Asterisk y FreePBX, que se utilizan en la creación de centrales telefónicas modernas. Se automatizan estas instalaciones mediante la herramienta Chef y se realizan llamadas a través de clientes de SIP compatibles con dispositivos móviles.
​	Además, se implementan servidores Apache, ampliamente reconocidos para el alojamiento de sitios web basados en el protocolo HTTP. Se configuran dichos servidores en ambas redes, generando páginas HTML sencillas que denotan su funcionalidad. Al igual que en las secciones anteriores, se prioriza la automatización de estas instalaciones utilizando herramientas de administración de configuración.

# Explicación de cada sub parte (AWS, Asterisk, Http server)
​	En esta sección se dará una breve explicación sobre las herramientas utilizadas en el proyecto.

## Implementación en AWS (Amazon Web Services)
​	Se utiliza Amazon Web Services (AWS) para crear y configurar una red virtual. Utilizando la herramienta Terraform, se definen y despliegan las infraestructuras como código, lo que permite la creación de redes públicas y privadas con subredes.
La implementación en AWS proporciona una base sólida para entender los conceptos fundamentales de la nube, la gestión de recursos y la automatización de infraestructura.

## Configuración de Asterisk y FreePBX

​	En esta segunda parte del proyecto,se trabaja con Asterisk y FreePBX. Estas herramientas permiten el desarrollo de centrales telefónicas, aprovechando el protocolo de capa de sesión SIP y el protocolo de transporte UDP.
​	Se automatiza la instalación y configuración de Asterisk y FreePBX utilizando la herramienta Chef. De esta manera se facilita la implementación y ayuda a comprender cómo se pueden administrar sistemas y aplicaciones de manera eficiente. Se crean extensiones SIP y se permite realizar llamadas a través de clientes compatibles con dispositivos móviles. 
​	Es de esta manera que se permite experimentar y entender el funcionamiento de la telefonía IP en un entorno controlado.

## Configuración de Servidores HTTP (Apache Server)

​	La tercera parte del proyecto se centra en la implementación de servidores web Apache. Se instalan y configuran dos servidores Apache en diferentes máquinas virtuales, una en la red pública y otra en la red privada. Estos servidores exponen páginas web sencillas con el mensaje "Server 1" y "Server 2". Nuevamente, la instalación y configuración se automatiza.

# Diagramas de arquitectura

xximagenxx

# Diagramas de flujo

xxiamgenxx

# Instrucciones de Ejecución

​	A continuación se explicará brevemente cómo ejecutar la versión final del programa, se adjuntan de igual manera imágenes con la intención de facilitar el entendimiento de la explicación:

​	Para este proyecto el código utilizado se ejecuta en consola, se hace uso de la herramienta Visual Studio Code para tener acceso a la extensión AWS ToolKit for VS Code. Se recomienda hacer uso de estas mismas herramientas para la ejecución del mismo.

xximagenxx

​	En la extensión de AWS se colocan las siguientes credenciales que pertenecen al compañero Ángel (esto debido a que estamos utilizando únicamente la credencial de esta persona).

xximagenxx

​	Para poder hacer uso de este proyecto es necesario tener instalada la herramienta Terraform en su última versión.

​	Se ejecuta el siguiente comando, en la terminal de Visual Studio Code: npm install terraform

​	Luego se ejecuta el comando: terraform init
​	Luego se ejecuta el comando: terraform apply (el apply actualiza el estado de la infraestructura)
​	Esto crea la infraestructura y se puede crear una conexión por ssh a la máquina virtual.

​	Para conectarse mediante ssh es necesario utilizar el mainkey en el root del usuario.
​	Si no se cuenta con un key se puede crear uno nuevo.
​	Este mainkey tiene que ser agregado a la instancia de AWS donde se va a realizar la conexión por ssh.
​	Luego se actualiza la infraestructura de nuevo con: terraform apply -auto-approve
​	Una vez guardado el mainkey se puede utilizar el comando: ssh -i ~/.ssh/[nombre del archivo de la clave privada] ubuntu@[ip/dns de la instancia pública] para conectarse a la instancia pública.
​	Una vez establecida la conexión con la máquina virtual de la instancia pública es posible ejecutar comandos de linux sobre esta consola que afectan la máquina virtual.
​	Como las máquinas virtuales son creadas con un imagen que ya tiene instalados con los programas necesarios, solo se debe de hacer un pull del repositorio de github que guarda los repositorios de chef. 
Sobre el root se ejecuta el comando: git clone https://github.com/DavidEspinozaNemo/2023-02-2016012024-IC7602.git.
​	Una vez descargado el repositorio se accede al repositorio de chef público con: cd 2023-02-2016012024-IC7602/Proyecto0/chef-repo_public
​	Una vez dentro del chef repo público se va a ejecutar el comando: sudo chef-solo -c solo.rb -j node.json. 	Esto lo que causa es que el runlist del chef de repo se ejecute, iniciando los servicios de asterisk, apache server y pbx en la instancia pública.
​	Después de haberse ejecutado el chef en la instancia pública se va a hacer una conexión ssh desde la instancia de la red pública a la de la privada. Utilizando el comando ssh -i ~/.ssh/[nombre del key].crash ubuntu@[ip de la máquina privada].
​	Una vez conectado a la instancia de la maquina virtual de la red privada se clona el repositorio en esta maquina utilizando el comando: git clone https://github.com/DavidEspinozaNemo/2023-02-2016012024-IC7602.git.
​	Una vez descargado el repositorio se accede al repositorio de chef privado con: cd 2023-02-2016012024-IC7602/Proyecto0/chef-private
​	Ya dentro del repositorio de chef privado se ejecuta el comando: sudo chef-solo -c solo.rb -j node.json. Lo que ejecuta el runlist del chef repo

# Pruebas Unitarias 

​	A continuación, se presenta un resumen conciso de algunas pruebas unitarias llevadas a cabo en el proyecto, detallando el nombre de cada prueba, una breve descripción de su propósito y los resultados obtenidos tras su ejecución.
## Prueba 01: Conectividad entre usuarios SIP

​	Una vez teniendo el servidor FreePBX funcionando debemos realizar una prueba de conectividad entre dos clientes SIP, la prueba consiste en crear un cliente en una máquina virtual y llamar a otro cliente a través del servicio almacenado en AWS.

### Pasos de la creación

​	Una vez instalados los paquetes, en el buscador web debemos poner: dirección ip / admin para acceder la página administradora de FreePBX.

​	Luego crear una extensión SIP.
​	Nos vamos a la opción All Extencion > add extencion > add new SIP extencion

​	Aquí solo debemos poner un número cualquiera en el user extencion como 666, el resto de la información es relleno que debe estar presente, y presionamos submit.

​	Luego debes descargar un cliente SIP como Zoiper5 o Jami, lo descargamos de la página de Ubuntu Software, buscando Cliente SIP.

​	Primero creamos una cuenta cualquiera, y nos vamos a la opción de Add Acouds > advance Features > Configure a SIP account.

​	Habilitamos la opción de UDP, en el server ponemos 127.0.0.1, en el user utilizamos la extensión previamente creada (666) con su contraseña (una fácil como hola o 1234). 

​	Y así en el cliente, a través de la extensión SIP, y se habilita la opción de hacer llamadas.

### Resultados 

​	No pudimos concretar la llamada.

xxiamgenxx

## Prueba 02: Inicialización de las páginas Http

En esta prueba simplemente debemos abrir las páginas https creadas en la subnet pública y en la subnet privada para comprobar si hay errores en su ejecución. Comprobar que el acceso por hacia la pública se pueda realizar por medio de internet y el acceso de la segunda sólo sea posible a través de la subnet pública.

### Pasos de la creación

### Resultados 

## Prueba 03: Configuraciones de la máquina virtual en AWS

…

### Pasos de la creación



### Resultados 



# Recomendaciones y conclusiones

( x10 )
Recomendación en cualquier ámbito, como la comprobación de las versiones de las aplicaciones.

Durante la fase de instalación nos topamos con errores que no permitían instalar las dependencias de Asterisk, resulta que las versiones eran incompatibles. Teníamos por defecto la versión 8.0 de php cuando para las dependencias de Asterisk se necesitaba la versión 5.2, así que tuvimos que reinstalar php y otras dependencias. Se recomienda revisar las compatibilidades a la hora de llevar a cabo dichas acciones.
Si durante la instalación de las aplicaciones necesarias surgen errores en Windows, se recomienda utilizar “chocolatey”, que es un administrador de paquetes de Windows de línea de comandos. Esta recomendación viene de errores que surgieron durante la instalación del proyecto en un computador específico.
Para facilitar el uso de terraform instalar la extensión de Visual Studio Code llamada “HashiCorp Terraform”.
Hay que utilizar la clave con la extensión .pub que es la pública, si se crea con la llave privada AWS tirar un error, a la hora de crear la conexión. Se recomienda tener bien identificadas desde el principio dichas claves pues por experiencia propia esto puede generar problemas a futuro.
Realizar una imagen de la máquina virtual para guardar versiones de lo trabajado y volver a una segura si se comete algún error.
Al hacer uso de Windows se complicó significativamente el progreso con respecto a las instalaciones de dependencias y herramientas necesarias para el proyecto. Sin embargo, haciendo uso de Linux el caso fue diferente, es por ello que se recomienda evitar utilizar Windows para este proyecto.
En las recetas de Chef cuando se ingresan comandos se puede presentar errores debido a que se necesita la aprobación de una instalación (por ejemplo)



# Referencias Bibliográficas



Chef-solo (executable). (s. f.-b). Progress Chef. Recuperado 17 de agosto de 2023, de https://docs.chef.io/ctl_chef_solo/

Asterisk Cookbook - Chef Supermarket. (2014, 26 agosto). CHEF SUPERMARKET. Recuperado 17 de agosto de 2023, de https://supermarket.chef.io/cookbooks/asterisk

Jethva, H. (2022). How to install FreePBX on Ubuntu 20.04 (Open Source PBX tutorial). Cloud Infrastructure Services. https://cloudinfrastructureservices.co.uk/how-to-install-freepbx-on-ubuntu-20-04/

freeCodeCamp.org. (2022, 11 abril). Learn terraform (and AWS) by building a dev environment – full course for beginners [Vídeo]. YouTube. https://www.youtube.com/watch?v=iRaai1IBlB0

Install Terraform | Terraform | HashiCorp Developer. (s. f.). Install Terraform | Terraform | HashiCorp Developer. https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli

Crosstalk Solutions. (2021, 18 junio). 01 PBX Planning - FreePBX 101 V15 [Vídeo]. YouTube. https://www.youtube.com/watch?v=l30WKTYf9ZY



