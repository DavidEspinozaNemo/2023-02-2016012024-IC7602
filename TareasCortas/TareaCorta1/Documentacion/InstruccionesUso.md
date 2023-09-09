# Instrucciones para uso del programa.

Windows

- Instalación de python 3.11 
- Utilizar la consola para escribir el siguiente comando e instalar venv “python -m venv my_venv”
- En la consola escribir el comando “ .venv/bin/activate” para abrir el entorno virtualInstalar las dependencias del ambiente con el comando “pip install -r ./requirements.txt”
- Para usar la grabadora de voz correr el archivo con el comando “grabadora.py”
  - Dentro de la grabadora se puede iniciar una grabación con el botón Iniciar.
  - Detener la grabación con el botón parar. Esto crea el archivo atm de la grabación.
  - Pausar la grabación con el botón pausar.
  - Las grabaciones quedan guardadas en el folder seleccionado con el explorador de archivos que se abre al tocar el botón de carpeta.
- Para abrir el reproductor de archivos .atm correr el comando “python reproductor.py”
- Esto inicia una página web que puede ser accedida ingresando a la dirección de localhost en el navegador web. Direccion: http://127.0.0.1:5000/
  - Esperar a que carguen los gráficos.
  - Usar play para reproducir el sonido. 
  - Usar rewind para moverse hacia atrás en el archivo.
  - Usar forward para moverse hacia adelante en el archivo.
  - Reset zoom
  - Reset chart

Limitaciones del programa

- El programa no puede grabar más de 15 segundos.
- El programa no lee archivos wav. Solo funciona con la grabación de voz

## Referencias:

- Programacionpython. (2020, 10 noviembre). GRABACIÓN DE SONIDO CON «Pyaudio» (ejercicio en Python). El Programador Chapuzas. https://programacionpython80889555.wordpress.com/2018/10/16/grabacion-de-sonido-con-pyaudio-ejercicio-basico-en-python/Fourier 
- Transforms (SciPy.FFT) — SciPY v1.11.2 Manual. (s. f.). https://docs.scipy.org/doc/scipy/tutorial/fft.html
- Sistemas Inteligentes. (2020, 19 noviembre). Transformada discreta de Fourier. Análisis de audio en tiempo real con Python (SCipy) [Vídeo]. YouTube. https://www.youtube.com/watch?v=5QPdlTg1z-I