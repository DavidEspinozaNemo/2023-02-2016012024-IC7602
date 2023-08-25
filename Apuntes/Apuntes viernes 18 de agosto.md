![eLogo TEC](https://www.tec.ac.cr/sites/default/files/media/logo_tec.jpg)

##### Escuela de ingeniería en computación
##### Redes 
##### Apuntes viernes 18 de agosto
##### Profesor: Gerardo Nereo Campos Araya
---
# **Sobre la tarea:**
Autrum -> el profe se inventó ese nombre. Así que no nos volvamos locos buscando en internet.
El lenguaje seguro para implementar la tarea es Python.
---
###### Nota: Siempre tenemos pérdida de armónicos y debido a esto perdemos parte de la calidad del audio que estamos escuchando. Hay micrófonos que se usan por ejemplo en podcast que ayudan a mejorar la calidad del audio.
---
1. Se puede hacer pruebas con mp3 y documentarla.
2. Se puede hacer completamente en consola o con interfaz gráfica
3. Al ser el dominio de frecuencia distinto al dominio del tiempo podemos grabar 5 segundos y mostrar el gráfico (y repetimos).
4. EL profe ocupa que llevemos algún tipo de archivo que nos permita sincronizar el dominio de frecuencia con el del tiempo.
5. El profe mostró un código que dice nos puede pasar. El código genera ondas en frecuencias específicas y genera gráfico en base a eso. Dependiendo de los cambios que hagamos se emite un sonido y un gráfico diferentes.
5. En las transmisiones tenemos ondas que se suman entre ellas y deforman el espectro de la señal que se está mandando y así tienen la posibilidad de llegar más largo.
7. No hace falta hacer las pruebas con varios micrófonos. Basta con un estándar.
8. Hacer la documentación diciendo exactamente qué es lo que necesita el profe para correr la tarea. ¡Incluso las versiones que necesita!

# **Sobre la materia:**
## Métodos de transmisión guiado:
Permiten tener mucho aislamiento del ambiente y así podemos reducir la probabilidad de perder componentes armónicos. así la señal se debilita menos rápido y podemos hacer transmisiones a mayor distancia.
Los dispositivos guiados tienen características de trenzado, coraza, blindaje, etc y la fibra óptica se sale un poquito de la canasta.
Recordemos que existe el monomodo y el multimodo (el que se suele trabajar en área residencial) y que el multimodo hace que los haces de luz salen con un ángulo y van rebotando, causando que tarde un poco más en llegar la información.
## Medios de transmisión inalámbrica:
### Espectro electromagnético: 
Ondas electromagnéticas que se generan por el movimiento de electrones. 
Cuando agarramos y conectamos un circuito a la antena podemos modificar y difundir ondas electromagnéticas que un receptor puede captar dependiendo de la geometría de la antena.
---
###### Nota: Cuando conectamos audífonos estos se convierten en antena. Solemos pensar que una antena es un monopolo y como las de televisión que había antes.  Pero recordemos que las ondas cuando son enviadas salen en todos los ángulos y se van moviendo por el aire, esta onda es recibida por pedacitos en el aire y así la va generando. Los audífonos de amplitud modulada es un cuarto de la amplitud de la onda.
---
###### Nota: Los teléfonos utilizan fractales y hacen que en el circuito del teléfono haya líneas de cobre unidas que tienen el tamaño de un cuarto de longitud de onda. Este recibe los fragmentos de ondas.
---
![Antenas parabolicas para micoondas](https://4.bp.blogspot.com/-mwGSN5UUcUk/WLcpsKHWTaI/AAAAAAAADys/tmsn2vlNZ1kzcWLcO8PARnIRwrhuM-lMQCLcB/s1600/AntenaDipolo.jpg)
¿Las antenas solo deben tener una forma? No, la forma de las antenas define el tipo de ondas que puede recibir y con qué potencia puede recibirlas.
![Antenas parabolicas para micoondas](https://solnaciente.com/wp-content/uploads/2021/12/612-613591.jpg)
Cuando hacemos una transmisión esta va viajando y tiene problemas de retardo porque no todos los componentes de onda pueden viajar al mismo tiempo o no se pueden mandar todos ni pueden viajar tanto tiempo por un material. Esto afecta el ancho de banda y la cantidad de información que podemos transmitir. 
### En el espectro electromagnético:
Tenemos el ancho y largo de la onda. Dependiendo de la frecuencia de esta las ondas van a ser mas grandes, habrá mayor amplitud y la onda va a poder viajar en el espacio durante más tiempo con menos frecuencia. 
Dependiendo del tamaño de la onda se puede dar un problemita: 
¿Por qué no podía comunicarme en ambas vías? Las longitudes de onda son tan grandes que la potencia que se requiere para hacer una transmisión es muy alta y las personas no las tienen disponibles. Si la devolvemos la onda va a causar interferencia, chocar con otras señales y dañar la comunicación.
Entre más baja es la longitud de ondas más potencia necesita para viajar.
### Radiotransmisión: 
Transmisiones AM y FM. Tienen poca atenuación.  Una transmisión de onda terrestre en am sigue la curvatura de la tierra mientras que en FM sube y rebota (no dejan el planeta) permitiendo que se cubran distancias más grandes. 
### Microondas: 
Las hondas deben viajar en línea recta. Para esto ocupamos el concepto “línea vista” que quiere decir que las antenas deben estar alineadas y verse entre ellas. Un problema sería que se meta un obstáculo entre las 2 antenas tapando la línea vista.
La otra opción es hacer un reflejo en el suelo, pero en áreas urbanas no se puede hacer.
![Antenas parabolicas para micoondas](https://www.comunicacionesinalambricashoy.com/imagenes/2022/01/kp-mesh-dish-antenna-lp.jpg)
Se utilizan antenas microondas para hacer transmisiones con microondas. El plato que tienen causa que donde se dispara la transmisión rebota contra el plato en línea recta con mayor potencia en la señal.
### Industrial, Scientific, Media (ISM): 
Son bandas que no ocupan licencia y no están reguladas. Pero a nivel internacional existen regulaciones que no permiten hacer transmisiones en altas potencias, por lo que la señal no llega tan largo y no hace interferencia a otras personas.
