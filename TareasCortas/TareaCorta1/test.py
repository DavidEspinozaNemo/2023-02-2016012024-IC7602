import matplotlib.pyplot as plt
import pyaudio as pa 
import struct 
import numpy as np

FRAMES = 1024*8
FORMAT = pa.paInt16
CHANNELS = 1
Fs = 44100

p = pa.PyAudio()

stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=Fs,
    input=True,
    output=True,
    frames_per_buffer=FRAMES
)

fig, (ax, ax1) = plt.subplots(2)

x_audio = np.arange(0, FRAMES, 1)
x_fft = np.linspace(0, Fs, FRAMES)

line, = ax.plot(x_audio, np.random.rand(FRAMES), 'r')
line_fft, = ax1.semilogx(x_fft, np.random.rand(FRAMES), 'b')

ax.set_ylim(-32500, 32500)
ax.set_xlim(0, FRAMES)

Fmin = 1
Fmax = 5000
ax1.set_xlim(Fmin, Fmax)

fig.show()

F = (Fs/FRAMES)*np.arange(0, FRAMES//2)

while True:
    data = stream.read(FRAMES)
    dataInt = struct.unpack(str(FRAMES) + 'h', data)
    
    line.set_ydata(dataInt)
    
    M_gk = abs(np.fft.fft(dataInt)/FRAMES)
    
    ax1.set_ylim(0, np.max(M_gk+10))
    line_fft.set_ydata(M_gk)
    
    M_gk = M_gk[0:FRAMES//2]
    Posm = np.where(M_gk == np.max(M_gk))
    F_fund = F[Posm]
    
    print(int(F_fund))
    
    fig.canvas.draw()
    fig.canvas.flush_events()
