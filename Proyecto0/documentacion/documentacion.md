![Image del logo del Tec](logo-tec.jpg)

# Escuela de Ingeniería en Computación

## Proyecto opcional 

### Redes

Profesor: **Gerardo Nereo Campos Araya**

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

A continuación se muestra el diagrama de arquitectura.

![Diagrama de arquitectura](diagrama-arq.jpg)

# Diagramas de flujo

A continuación se muestra el diagrama de flujo.

![Diagrama de flujo](diagrama-flujo.jpg)

# Instrucciones de Ejecución

​	A continuación se explicará brevemente cómo ejecutar la versión final del programa, se adjuntan de igual manera imágenes con la intención de facilitar el entendimiento de la explicación:

​	Para este proyecto el código utilizado se ejecuta en consola, se hace uso de la herramienta Visual Studio Code para tener acceso a la extensión AWS ToolKit for VS Code. Se recomienda hacer uso de estas mismas herramientas para la ejecución del mismo.

![AWS Toolkit](aws-toolkit.jpg)

​	En la extensión de AWS se colocan las siguientes credenciales que pertenecen al compañero Ángel (esto debido a que estamos utilizando únicamente la credencial de esta persona).

![Extención de llave](key-extension.jpg)

​	Para poder hacer uso de este proyecto es necesario tener instalada la herramienta Terraform en su última versión.

​	Se ejecuta el siguiente comando, en la terminal de Visual Studio Code: npm install terraform

  Luego se ejecuta el comando: terraform init
  
  Luego se ejecuta el comando: terraform apply (el apply actualiza el estado de la infraestructura)
  
  Esto crea la infraestructura y se puede crear una conexión por ssh a la máquina virtual.

  Para conectarse mediante ssh es necesario utilizar el mainkey en el root del usuario.
  
  Si no se cuenta con un key se puede crear uno nuevo.

  Este mainkey tiene que ser agregado a la instancia de AWS donde se va a realizar la conexión por ssh.

  Luego se actualiza la infraestructura de nuevo con: terraform apply -auto-approve

  Una vez guardado el mainkey se puede utilizar el comando: ssh -i ~/.ssh/[nombre del archivo de la clave privada] ubuntu@[ip/dns de la instancia pública] para conectarse a la instancia pública.

  Una vez establecida la conexión con la máquina virtual de la instancia pública es posible ejecutar comandos de linux sobre esta consola que afectan la máquina virtual.

  Como las máquinas virtuales son creadas con un imagen que ya tiene instalados con los programas necesarios, solo se debe de hacer un pull del repositorio de github que guarda los repositorios de chef. 

  Sobre el root se ejecuta el comando: git clone https://github.com/DavidEspinozaNemo/2023-02-2016012024-IC7602.git.

  Una vez descargado el repositorio se accede al repositorio de chef público con: cd 2023-02-2016012024-IC7602/Proyecto0/chef-repo_public

  Una vez dentro del chef repo público se va a ejecutar el comando: sudo chef-solo -c solo.rb -j node.json. Esto lo que causa es que el runlist del chef de repo se ejecute, iniciando los servicios de asterisk, apache server y pbx en la instancia pública.

  Después de haberse ejecutado el chef en la instancia pública se va a hacer una conexión ssh desde la instancia de la red pública a la de la privada. Utilizando el comando ssh -i ~/.ssh/[nombre del key].crash ubuntu@[ip de la máquina privada].

  Una vez conectado a la instancia de la maquina virtual de la red privada se clona el repositorio en esta maquina utilizando el comando: git clone https://github.com/DavidEspinozaNemo/2023-02-2016012024-IC7602.git.

  Una vez descargado el repositorio se accede al repositorio de chef privado con: cd 2023-02-2016012024-IC7602/Proyecto0/chef-private

  Ya dentro del repositorio de chef privado se ejecuta el comando: sudo chef-solo -c solo.rb -j node.json. Lo que ejecuta el runlist del chef repo privado y esto instala y configura el apache server que contiene el html que dice server2.

  Una vez finalizados estos pasos deberían estar creadas las dos instancias y se debería poder acceder desde cualquier navegador a la instancia pública. Al entrar en la instancia pública mediante el navegador, se debería de ver una página en html que dice Server1. 

  Al agregar la extensión /admin al ip de la máquina pública en la barra de búsqueda del navegador se abre el acceso a la página de administración de pbx.

  En la página de administración se puede entrar en el primer botón de izquierda a derecha para la parte de administración.

  Ahí se pueden crear las extensiones SIP como se indican en las pruebas unitarias.

  Una vez creadas las extensiones SIP es necesario descargar algún cliente SIP en un dispositivo móvil para agregar la extensión del cliente SIP.

  Una vez se tengan dos extensiones en dos clientes se pueden realizar llamadas telefónicas entre los clientes SIP.

# Pruebas Unitarias 

​	A continuación, se presenta un resumen conciso de las tres pruebas unitarias llevadas a cabo en el proyecto, detallando el nombre de cada prueba, una breve descripción de su propósito y los resultados obtenidos tras su ejecución.

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

![Resultado 1](call-no-found.jpg)

## Prueba 02: Inicialización de las páginas Http

Para la segunda prueba, se realizó una verificación de las páginas web generadas en las subredes pública y privada mediante el acceso a través de protocolo HTTPS. El propósito es identificar posibles irregularidades en la ejecución. Es imperativo confirmar que el acceso a la subred pública pueda llevarse a cabo utilizando la infraestructura de internet, mientras que el acceso a la segunda subred esté restringido exclusivamente a través de la subred pública.

### Pasos de la creación

En primera instancia, se realizó un proceso de descarga y configuración de Asterisk , FreePBX y Chef, para este se presentaron múltiples errores lo cuales se buscaron solucionar con la ayuda del profesor por medio de una reunión realizada con él el día 15 de agosto. Además se siguieron los pasos suministrados por la documentación oficial de los respectivos sitios.

Seguidamente, para la creación de la primera subnet se creó una instancia en AWS con las “golden image” creadas en el paso anterior y se realizó una receta con la herramienta Chef la cual se encargaba de llevar a cabo la descarga de apache y  montar el servidor 1 (público) sobre la máquina virtual de AWS.

Nota: Recordar que esta primera subnet es accesible por medio de internet por lo cual solo se debe de buscar la dirección ip pública en el navegador de preferencia.

Finalmente, la creación de la instancia privada solamente requiere de una imagen con los paquetes de chef ya que esta no necesita ni el Asterisk ni el FreePBX, de igual forma se ejecuta una receta por medio de la herramienta chef con la cual se instala apache y se configura el servidor 2.

### Resultados 

La prueba fue aprobada, como se puede visualizar en los siguientes recursos visuales, se desplegó y configuró de manera correcta el servidor.

## Prueba 03: Creación de la infraestructura en AWS

La tercera y última prueba se basa en la creación de las dos instancias (máquinas virtuales) en el servicio de AWS, para este proceso se utilizó Terraform y se siguieron una serie de pasos que se pueden ver a detalle a continuación.

Inicialmente, la primera acción fue crear y configurar adecuadamente una cuenta dentro de los servicios de AWS, recolectando la información más relevante dentro de un archivo (claves de acceso SSH, usuario, contraseña, dirección).

Seguidamente, se inició con el uso de terraform que es la herramienta que utilizamos para definir y administrar nuestra infraestructura como código. Para su instalación se utilizó el comando *brew* para el caso de Linux y Choco en el caso de Windows.

Una vez instalado y con el ambiente funcional se procedió a crear el archivo .tf en el cual se definió la infraestructura del servicio, el proveedor de AWS y se definió la instancia. 

Al finalizar su creación se ejecutan una serie de comandos donde se inicializa un proyecto de terraform, se ve la vista previa del servicio y finalmente se ejecuta con *apply*.

Realizado todo el proceso se puede ingresar al sitio web de AWS y comprobar que el ambiente fue creado con éxito.

Los resultados de esta prueba fueron exitosos y por medio de las evidencias disponibles más adelante se puede visualizar como fueron creadas las instancias por medio de Terraform y con el servicio de nube de Amazon AWS.

Paso 4: Definición del Proveedor de AWS

![captura 1](public_instance_created.jpg)

![captura 2](others_components_created.jpg)

![captura 3](others_components_created2.jpg)

![captura 4](others_components_created3.jpg)

![captura 5](others_components_created4.jpg)

![captura 6](others_components_created5.jpg)

### Resultados 

Los resultados de esta prueba fueron exitosos y por medio de las evidencias disponibles más adelante se puede visualizar como fueron creadas las instancias por medio de Terraform y con el servicio de nube de Amazon AWS.

![Resultado 3](aws-maquine.jpg)

# Recomendaciones y conclusiones

Recomendación en cualquier ámbito, como la comprobación de las versiones de las aplicaciones.

1. Durante la fase de instalación nos topamos con errores que no permitían instalar las dependencias de Asterisk, resulta que las versiones eran incompatibles. Teníamos por defecto la versión 8.0 de php cuando para las dependencias de Asterisk se necesitaba la versión 5.2, así que tuvimos que reinstalar php y otras dependencias. Se recomienda revisar las compatibilidades a la hora de llevar a cabo dichas acciones.
2. Si durante la instalación de las aplicaciones necesarias surgen errores en Windows, se recomienda utilizar “chocolatey”, que es un administrador de paquetes de Windows de línea de comandos. Esta recomendación viene de errores que surgieron durante la instalación del proyecto en un computador específico.
3. Para facilitar el uso de terraform instalar la extensión de Visual Studio Code llamada “HashiCorp Terraform”.
4. Hay que utilizar la clave con la extensión .pub que es la pública, si se crea con la llave privada AWS tirar un error, a la hora de crear la conexión. Se recomienda tener bien identificadas desde el principio dichas claves pues por experiencia propia esto puede generar problemas a futuro.
5. Realizar una imagen de la máquina virtual para guardar versiones de lo trabajado y volver a una segura si se comete algún error.
6. Al hacer uso de Windows se complicó significativamente el progreso con respecto a las instalaciones de dependencias y herramientas necesarias para el proyecto. Sin embargo, haciendo uso de Linux el caso fue diferente, es por ello que se recomienda evitar utilizar Windows para este proyecto.
7. En las recetas de Chef cuando se ingresan comandos se presentaron errores debido a que se necesitaba la aprobación de una instalación (por ejemplo), es por ello que se recomienda que en los comandos donde es necesario se agregue -y al final. De esta manera se aprueba automáticamente y no da problemas.
8. Se recomienda siempre eliminar o no dejar activa la máquina una vez terminadas las pruebas porque se gasta créditos y pueden llegar a cobrarnos dinero que no planeábamos gastar. Esto se recomienda a base de experiencia, pues se nos olvidó después de unas pruebas y si bien nos dimos cuenta a tiempo el aumento que se vio era significativo.
9. Se presentaron dificultades a la hora de realizar la automatización de Chef. Se recomienda que a la hora de elaborar la receta se comience con un conjunto pequeño para luego ir ampliando gradualmente para así tener mayor claridad y seguridad de haber abarcado lo necesario.
10. Se recomienda una buena comunicación si el equipo es grande y no dividir las asignaciones, esto debido a que los demás miembros se pueden quedar perdidos en la comprensión de ciertas áreas.

El proceso de desarrollo de este proyecto ha proporcionado una valiosa serie de lecciones y recomendaciones que son esenciales para abordar de manera efectiva tareas similares en el futuro. A través de los desafíos y logros experimentados, hemos fortalecido nuestro enfoque hacia la planificación, la implementación y la solución de problemas en distintas etapas del proyecto. A continuación, se resumen las conclusiones clave extraídas de este proceso:

1. Es bueno ir lento porque precisa: Es mejor comprender correctamente el proyecto a querer terminarlo todo de una vez sin saber qué es lo que se está haciendo.
2. Compatibilidad y versiones: La compatibilidad entre las distintas versiones de aplicaciones y dependencias es crucial. Los problemas que enfrentamos durante la instalación de dependencias de Asterisk resaltan la importancia de verificar las compatibilidades antes de proceder con cualquier acción.
3. Herramientas para la Gestión: El uso de herramientas específicas, como "chocolatey" en Windows o "HashiCorp Terraform" en Visual Studio Code, puede simplificar en gran medida la instalación y la administración de aplicaciones y recursos.
4. Administración de Claves: La correcta identificación y uso de las claves, tanto públicas como privadas, es esencial para evitar problemas futuros durante la configuración de conexiones seguras.
5. Backup y Versionado: La creación de imágenes de máquina virtual para guardar versiones seguras del trabajo realizado es esencial para revertir cambios en caso de errores o problemas imprevistos.
6. Elección de Plataforma: Basándonos en la experiencia, el uso de Linux demostró ser más adecuado para la instalación de dependencias y herramientas necesarias en comparación con Windows, lo que respalda la recomendación de optar por Linux en proyectos similares.
7. Automatización Gradual: Al llevar a cabo tareas de automatización, es recomendable comenzar con un alcance pequeño y ampliarlo gradualmente. Esto proporciona mayor claridad y seguridad en la implementación y evita abordar problemas complejos de manera prematura.
8. Control de Costos: Mantener un control riguroso sobre los recursos activos es fundamental para evitar gastos no previstos. Se recomienda desactivar o eliminar máquinas virtuales y recursos una vez finalizadas las pruebas.
9. Comunicación y Distribución de Tareas: En equipos grandes, la comunicación efectiva y la distribución adecuada de tareas son esenciales para garantizar que todos los miembros del equipo estén alineados en la comprensión del proyecto y su alcance.
10. Consultas: Si se tiene la posibilidad de realizar consultas a una persona de confianza, es mejor hacerlo. No es buena idea quedarse con las dudas por miedo o por sentir que todo lo puede hacer uno solo.


# Referencias Bibliográficas



Chef-solo (executable). (s. f.-b). Progress Chef. Recuperado 17 de agosto de 2023, de https://docs.chef.io/ctl_chef_solo/

Asterisk Cookbook - Chef Supermarket. (2014, 26 agosto). CHEF SUPERMARKET. Recuperado 17 de agosto de 2023, de https://supermarket.chef.io/cookbooks/asterisk

Jethva, H. (2022). How to install FreePBX on Ubuntu 20.04 (Open Source PBX tutorial). Cloud Infrastructure Services. https://cloudinfrastructureservices.co.uk/how-to-install-freepbx-on-ubuntu-20-04/

freeCodeCamp.org. (2022, 11 abril). Learn terraform (and AWS) by building a dev environment – full course for beginners [Vídeo]. YouTube. https://www.youtube.com/watch?v=iRaai1IBlB0

Install Terraform | Terraform | HashiCorp Developer. (s. f.). Install Terraform | Terraform | HashiCorp Developer. https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli

Crosstalk Solutions. (2021, 18 junio). 01 PBX Planning - FreePBX 101 V15 [Vídeo]. YouTube. https://www.youtube.com/watch?v=l30WKTYf9ZY



