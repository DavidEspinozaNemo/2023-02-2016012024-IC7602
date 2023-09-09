# Primera prueba para la implementación de los graficos  ajustados a los datos del audio.
# Algunos de los pasos son solamente recreados o simulados, el principal objetivo es probar la funcionalidad de los graficos 


import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

wav_file = './TareasCortas/TareaCorta1/Angel.wav'

# Leer el archivo WAV
wav_array, sample_rate = sf.read(wav_file)

time = np.arange(0, len(wav_array)) / sample_rate

plt.figure(figsize=(12, 6))

# Formato para la gráfica del dominio del tiempo
plt.subplot(2, 1, 1)
plt.plot(time, wav_array)
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.title('Señal en el Dominio del Tiempo')

# Se calcula la transformada de Fourier
freq_data = np.abs(np.fft.fft(wav_array))
freq_data = freq_data[:len(freq_data) // 2]

# Se instancia el eje de la frecuencia
freq = np.fft.fftfreq(len(wav_array), 1.0 / sample_rate)
freq = freq[:len(freq) // 2] 

# Formato para la gráfica de Fourier
plt.subplot(2, 1, 2)
plt.plot(freq, freq_data)
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud')
plt.title('Señal en el Dominio de la Frecuencia')

plt.tight_layout()
plt.show()
