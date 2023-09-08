import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Ruta al archivo WAV
wav_file = './TareasCortas/TareaCorta1/WavFiles/mixkit-fast-rocket-whoosh-1714.wav'

# Leer el archivo WAV usando soundfile
wav_array, sample_rate = sf.read(wav_file)
t = np.linspace(0, len(wav_array) / sample_rate, len(wav_array))
print("WavArray" , wav_array)
print("Sample_rate", sample_rate)
print("t : ", t)

# Crea una figura y un subplot para el dominio del tiempo
fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_xlim(0, len(wav_array) / sample_rate)  # Ajusta los límites del eje x
ax.set_ylim(-1, 1)  # Ajusta los límites del eje y
ax.set_xlabel('Tiempo (s)')
ax.set_ylabel('Amplitud')
ax.set_title('Señal en el Dominio del Tiempo')

# Función de inicialización para la animación
def init():
    line.set_data([], [])
    return line,

# Función de actualización para la animación
def update(frame):
    x = t[:frame]
    y = np.pad(x, (0, frame - len(x)), 'edge')
    #print("x : ", x)
    #print("y:  ", y)
    line.set_data(x, y)
    return line,

'''
# Genera algunos datos de prueba (en este caso, una onda senoidal)
t = np.linspace(0, 10, 1000)  # Tiempo de 0 a 10 segundos
data = np.sin(2 * np.pi * 1 * t)  # Una onda senoidal de 1 Hz

# Crea una figura y un subplot para el dominio del tiempo
fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_xlim(0, 10)  # Ajusta los límites del eje x
ax.set_ylim(-1, 1)  # Ajusta los límites del eje y
ax.set_xlabel('Tiempo (s)')
ax.set_ylabel('Amplitud')
ax.set_title('Señal en el Dominio del Tiempo')

# Función de inicialización para la animación
def init():
    line.set_data([], [])
    return line,

# Función de actualización para la animación
def update(frame):
    x = t[:frame]
    y = data[:frame]
    line.set_data(x, y)
    return line,
'''

# Configura la animación
ani = FuncAnimation(fig, update, frames=len(wav_array), init_func=init, blit=True)

# Muestra la animación
plt.show()
