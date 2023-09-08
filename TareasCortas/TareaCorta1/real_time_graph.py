# Primera prueba para la implementación de los graficos  ajustados a los datos del audio.
# Algunos de los pasos son solamente recreados o simulados, el principal objetivo es probar la funcionalidad de los graficos 


import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sounddevice as sd


# Ruta al archivo WAV
wav_file = './TareasCortas/TareaCorta1/WavFiles/mixkit-fast-rocket-whoosh-1714.wav'

# Leer el archivo WAV usando soundfile
wav_array, sample_rate = sf.read(wav_file)

time = np.arange(0, len(wav_array)) / sample_rate
'''
plt.figure(figsize=(12, 6))

# Subplot para el dominio del tiempo
plt.subplot(2, 1, 1)
plt.plot(time, wav_array)
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.title('Señal en el Dominio del Tiempo')

# Valores de prueba para el dominio de la frecuencia
# Reemplaza esto con tus datos de Fourier reales
freq_data = np.abs(np.fft.fft(wav_array))
freq_data = freq_data[:len(freq_data) // 2]  # Tomar la mitad debido a la simetría

# Crear el eje de frecuencia para el dominio de la frecuencia
freq = np.fft.fftfreq(len(wav_array), 1.0 / sample_rate)
freq = freq[:len(freq) // 2]  # Tomar la mitad debido a la simetría

# Subplot para el dominio de la frecuencia
plt.subplot(2, 1, 2)
plt.plot(freq, freq_data)
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud')
plt.title('Señal en el Dominio de la Frecuencia')

plt.tight_layout()
plt.show()


'''
# Ruta al archivo WAV
wav_file = './TareasCortas/TareaCorta1/WavFiles/mixkit-fast-rocket-whoosh-1714.wav'

# Leer el archivo WAV usando soundfile
wav_array, sample_rate = sf.read(wav_file)

# Crear una figura y un subplot para el dominio del tiempo
fig, ax = plt.subplots(figsize=(12, 6))
line, = ax.plot([], [])
ax.set_xlim(0, len(wav_array) / sample_rate)
ax.set_ylim(-1, 1)
ax.set_xlabel('Tiempo (s)')
ax.set_ylabel('Amplitud')
ax.set_title('Señal en el Dominio del Tiempo')

# Función de inicialización para la animación
def init():
    line.set_data([], [])
    return line,

# Función de actualización para la animación
def update(frame):
    # Actualizar la línea con nuevos datos de audio
    start = int(frame * sample_rate)
    end = start + int(0.1 * sample_rate)  # Muestra 0.1 segundos a la vez
    x = np.linspace(start / sample_rate, end / sample_rate, end - start)
    y = wav_array[start:end]
    line.set_data(x, y)
    return line,

# Configurar la animación
animation = FuncAnimation(fig, update, frames=np.linspace(0, len(wav_array) / sample_rate, len(wav_array)),
                    init_func=init, blit=True)

# Reproducir el audio mientras se muestra la animación
sd.play(wav_array, sample_rate)

# Mostrar la animación
plt.show()
