# Primera prueba para la implementación de los graficos  ajustados a los datos del audio.
# Algunos de los pasos son solamente recreados o simulados, el principal objetivo es probar la funcionalidad de los graficos 

import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt

# Ruta al archivo WAV
wav_file = './TareasCortas/TareaCorta1/WavFiles/mixkit-fast-rocket-whoosh-1714.wav'

# Leer el archivo WAV usando soundfile
wav_array, sample_rate = sf.read(wav_file)

# Crear el tiempo para el eje x
time = np.linspace(0, len(wav_array) / sample_rate, num=len(wav_array))

# Graficar la señal en el dominio del tiempo
plt.figure(figsize=(12, 6))

# Gráfica en el dominio del tiempo
plt.subplot(2, 1, 1)
plt.plot(time, wav_array)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Waveform in Time Domain')
plt.grid(True)


# Calcular la Transformada de Fourier
freq = 1
amplitude = 1

# Gráfica en el dominio de la frecuencia
'''plt.subplot(2, 1, 2)
plt.plot(freq, amplitude)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.title('Frequency Domain')
plt.grid(True)
plt.tight_layout()
'''

plt.show()