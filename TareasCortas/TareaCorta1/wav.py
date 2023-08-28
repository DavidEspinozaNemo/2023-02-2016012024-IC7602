import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# Cargar archivo WAV
sample_rate, audio_data = wavfile.read('C:\\Users\\tania\\Desktop\\Violin.wav')

# Obtener la duración del audio en segundos
duration = len(audio_data) / sample_rate

# Graficar la forma de onda del audio en el dominio del tiempo
time = np.arange(0, duration, 1/sample_rate)
plt.plot(time, audio_data)
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.title('Forma de Onda del Audio')
plt.show()

# Calcular la Transformada de Fourier
frequencies = np.fft.fftfreq(len(audio_data), d=1/sample_rate)
fft_values = np.fft.fft(audio_data)
magnitude = np.abs(fft_values)

# Graficar la Transformada de Fourier en el dominio de frecuencia
plt.plot(frequencies, magnitude)
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Magnitud')
plt.title('Transformada de Fourier')
plt.show()
