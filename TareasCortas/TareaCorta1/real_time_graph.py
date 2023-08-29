# Primera prueba para la implementación de los graficos dinamicos y ajustados a los datos de audio.
# Algunos de los pasos son solamente recreados o simulados, el principal objetivo es probar la funcionalidad de los graficos 

import threading
import pickle
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy import fft
from matplotlib.animation import FuncAnimation

# Cargar el archivo .atm
with open('archivo.atm', 'rb') as file:
    data = pickle.load(file)

audio_data = data['audio']
time_data = data['time_data']
freq_data = data['freq_data']

# Configuración de la gráfica
fig, (ax1, ax2) = plt.subplots(2, 1)
line1, = ax1.plot([], [])
line2, = ax2.plot([], [])
ax1.set_xlim(0, len(audio_data))
ax2.set_xlim(0, len(freq_data)//2)

# Inicializar el grafico
def init():
    line1.set_data([], [])
    line2.set_data([], [])
    return line1, line2

def update(frame):
    line1.set_data(np.arange(len(time_data)), time_data)
    line2.set_data(np.linspace(0, len(freq_data)//2, len(freq_data)//2), freq_data)
    return line1, line2

ani = FuncAnimation(fig, update, frames=range(len(audio_data)),
                    init_func=init, blit=True, interval=100)

# Controlar la reproducción
def play_audio():
    sd.play(audio_data, fs)
    sd.wait()

def pause_audio():
    sd.stop()

play_thread = threading.Thread(target=play_audio)
pause_thread = threading.Thread(target=pause_audio)

# Botones de control
play_button = plt.Button(ax1, 'Play', color='lightgoldenrodyellow')
pause_button = plt.Button(ax1, 'Pause', color='lightgoldenrodyellow')

def play(event):
    play_thread.start()

def pause(event):
    pause_thread.start()

play_button.on_clicked(play)
pause_button.on_clicked(pause)

plt.show()
