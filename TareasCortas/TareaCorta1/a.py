import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, filedialog, Entry, StringVar, messagebox
import glob
import pyaudio
import os
import wave
import threading
import scipy.fft
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import atm
from scipy.fft import fft

ventana = Tk()
ventana.title('Grabadora Audio WAV')

class SharedData:
    def __init__(self):
        self.directorio_actual = StringVar()
        self.audio_data = []
        self.lock = threading.Lock()
        self.grabando = False
        self.reproduciendo = False
        self.pausado = False
        self.CHUNK = 1024
        self.data = ""
        self.stream = ""
        self.audio = pyaudio.PyAudio()
        self.f = ""
        self.contador = 0
        self.contador1 = 0
        self.contador2 = 0
        self.act_proceso = False
        self.proceso = None

shared_data = SharedData()

# Esta función restablece los contadores de tiempo contador, contador1 y contador2.
def clear_contador():
    shared_data.lock.acquire()
    shared_data.contador = 0
    shared_data.contador1 = 0
    shared_data.contador2 = 0
    shared_data.lock.release()

# La función dire establece el valor de la variable directorio_actual (directorio actual) de tipo StringVar en el directorio 
# de trabajo actual obtenido de os.getcwd().
def dire():
    shared_data.lock.acquire()
    shared_data.directorio_actual.set(os.getcwd())
    shared_data.lock.release()

"""La función iniciar se llama cuando se presiona el botón "Grabar". Configura el proceso de grabación de audio. Inicializa 
   un objeto PyAudio y establece grabando en True para indicar que la grabación está activa. También deshabilita los botones 
   mediante la función bloqueo y comienza varios hilos para manejar la grabación y el conteo de tiempo."""
def iniciar():
    shared_data.lock.acquire()
    clear_contador()
    audio = pyaudio.PyAudio()
    bloqueo('disabled')
    shared_data.grabando = True
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    shared_data.act_proceso = True
    archivo = "grabacion.wav"  # Cambiamos la extensión a WAV
    t1 = threading.Thread(target=grabacion, args=(FORMAT, CHANNELS, RATE, shared_data.CHUNK, audio, archivo))
    t = threading.Thread(target=cuenta)
    t1.start()
    t.start()
    shared_data.lock.release()

# Esta función toma un número c y lo devuelve con un cero inicial si es menor que 10. Se utiliza para formatear los minutos y
# segundos.
def formato(c):
    if c < 10:
        c = "0" + str(c)
    return c

"""La función cuenta actualiza la pantalla del temporizador mientras se graba o reproduce el audio. Actualiza la etiqueta con 
   el valor de tiempo actual basado en contador, contador1 y contador2"""
def cuenta():
    shared_data.lock.acquire()
    if not shared_data.pausado:
        shared_data.contador += 1
        if shared_data.contador == 60:
            shared_data.contador = 0
            shared_data.contador2 += 1
        if shared_data.contador2 == 60:
            shared_data.contador2 = 0
            shared_data.contador1 += 1

    time['text'] = str(shared_data.contador1) + ":" + str(formato(shared_data.contador2)) + ":" + str(formato(shared_data.contador))
    shared_data.proceso = time.after(1000, cuenta)
    shared_data.lock.release()


"""La función abrir se llama cuando se presiona el botón "Abrir". Permite al usuario seleccionar un archivo MP3 para
   reproducirlo. Inicializa la reproducción de audio y maneja el inicio de un hilo tanto para contar el tiempo como para 
   reproducir el audio."""
def abrir():
    shared_data.lock.acquire()
    clear_contador()
    open_archive = filedialog.askopenfilename(initialdir="/",
                 title="Seleccione archivo", filetypes=(("atm", "*.atm"),
                 ("all files", "*.*")))
    if open_archive != "":
        try:
            shared_data.reproduciendo = True

            #Insert atm load code.
            atmData, tempWAV = atm.load(open_archive)

            audio = pyaudio.PyAudio()
            shared_data.f = wave.open(tempWAV, "rb")
            shared_data.stream = audio.open(format=audio.get_format_from_width(shared_data.f.getsampwidth()),  
                channels=shared_data.f.getnchannels(),  
                rate=shared_data.f.getframerate(),
                output=True)
            shared_data.data = shared_data.f.readframes(shared_data.CHUNK)

            bloqueo('disabled')
            t = threading.Thread(target=cuenta)
            t.start()
            t2 = threading.Thread(target=reproduce)
            t2.start()
        except Exception as e:
            if hasattr(e, 'message'):
                messagebox.showwarning("ERROR", e.message)
            else:
                messagebox.showwarning("ERROR", e)
            messagebox.showwarning("ERROR", "No se pudo abrir el archivo especificado")
            shared_data.reproduciendo = False
    shared_data.lock.release()

"""La función reproduce se encarga de reproducir el archivo de audio seleccionado. Escribe continuamente datos de audio 
   en el flujo de salida hasta que se haya reproducido todo el archivo."""
def reproduce():
    shared_data.lock.acquire()
    while shared_data.data and shared_data.reproduciendo == True:  
        shared_data.stream.write(shared_data.data)  
        shared_data.data = shared_data.f.readframes(shared_data.CHUNK)  

    shared_data.stream.stop_stream()  
    shared_data.stream.close()  

    shared_data.audio.terminate()
    time.after_cancel(shared_data.proceso)
    bloqueo('normal')
    shared_data.lock.release()

"""La función bloqueo habilita o deshabilita los botones especificados cambiando su atributo state. Se utiliza para 
   controlar el comportamiento de los botones durante la grabación y la reproducción."""


def bloqueo(s):
    btnIniciar.config(state=s)
    btnDir.config(state=s)
    btnAbrir.config(state=s)


"""La función parar se llama cuando se presiona el botón "Parar". Detiene la grabación o la reproducción y restaura 
   la funcionalidad de los botones."""    
def parar():
    shared_data.lock.acquire()
    if shared_data.grabando:
        shared_data.grabando = False
        time.after_cancel(shared_data.proceso)
        clear_contador()
    elif shared_data.reproduciendo:
        shared_data.reproduciendo = False
    bloqueo('normal')
    shared_data.lock.release()

"""La función direc se activa cuando se presiona el botón "Carpeta". Abre un cuadro de diálogo de carpeta para
   permitir al usuario elegir un directorio. Si se selecciona un directorio, cambia el directorio de trabajo actual y 
   actualiza la visualización del directorio utilizando la función dire."""
def direc():
    directorio = filedialog.askdirectory()
    if directorio != "":
        os.chdir(directorio)
        dire()
        
# Crear figuras para las gráficas en tiempo real
fig_signal, ax_signal = plt.subplots(figsize=(4, 2))
canvas_signal = FigureCanvasTkAgg(fig_signal, master=ventana)
canvas_signal.get_tk_widget().place(x=500, y=110)

fig_spectrum, ax_spectrum = plt.subplots(figsize=(4, 2))
canvas_spectrum = FigureCanvasTkAgg(fig_spectrum, master=ventana)
canvas_spectrum.get_tk_widget().place(x=10, y=110)

# Función para inicializar la gráfica de la señal
def init_signal():
    ax_signal.set_xlabel('Tiempo (muestras)')
    ax_signal.set_ylabel('Amplitud')
    ax_signal.set_title('Señal de audio en tiempo real')
    ax_signal.grid(True)
    return ax_signal,

# Función para actualizar la gráfica de la señal en tiempo real
def update_signal(frame):
    ax_signal.clear()
    with  shared_data.lock:
        ax_signal.plot(shared_data.audio_data, color='blue')
    return ax_signal,

# Función para inicializar la gráfica de la transformada de Fourier
def init_spectrum():
    ax_spectrum.set_xlabel('Frecuencia (Hz)')
    ax_spectrum.set_ylabel('Amplitud')
    ax_spectrum.set_title('Transformada de Fourier en tiempo real')
    ax_spectrum.grid(True)
    return ax_spectrum,

# Función para actualizar la gráfica de la transformada de Fourier en tiempo real
def update_spectrum(frame):
    ax_spectrum.clear()
    with shared_data.lock:
        if len(shared_data.audio_data) > 0:
            audio_array = np.array(shared_data.audio_data)
            audio_spectrum = np.abs(scipy.fft.fft(audio_array))
            audio_freqs = scipy.fft.fftfreq(len(audio_spectrum))
            ax_spectrum.plot(audio_freqs, audio_spectrum, color='green')
    return ax_spectrum,


# Crear animaciones para las gráficas
# Crear animaciones para las gráficas
signal_animation = FuncAnimation(fig_signal, update_signal, init_func=init_signal, blit=True, cache_frame_data=False)
spectrum_animation = FuncAnimation(fig_spectrum, update_spectrum, init_func=init_spectrum, blit=True, cache_frame_data=False)


def grabacion(FORMAT, CHANNELS, RATE, CHUNK, audio, archivo):
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []

    while shared_data.grabando == True:
        if not shared_data.pausado:
            data = stream.read(CHUNK)
            frames.append(data)
            
            # Captura los datos de audio en tiempo real para graficarlos
            audio_array = np.frombuffer(data, dtype=np.int16)
            with shared_data.lock:
                shared_data.audio_data.extend(audio_array)
        else:
            # Agregar algún tipo de pausa aquí, si deseas
            pass

    # DETENEMOS GRABACIÓN
    stream.stop_stream()
    stream.close()
    audio.terminate()

    grabs = glob.glob('*.*')

    # CREAR/GUARDAR EL ARCHIVO DE AUDIO EN FORMATO ATM
    count = 0
    for i in grabs:
        if "grabacion" in i:
            count += 1
    
    nombreDeArchivo = "grabacion" + "(" + str(count) + ")"

    if count > 0:
        archivo = nombreDeArchivo + ".wav"  # Cambiamos la extensión a WAV

    wf = wave.open(archivo, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    #DATA EXAMPLE
    #Save audio data in a dicctionary
    fix = np.array(shared_data.audio_data)
    d = fix.tolist()
    fourier_data = fft(d)
    data = {
        "audioData" : d,
        "fourierData": {
            "real": fourier_data.real.tolist(),
            "imag": fourier_data.imag.tolist(),
        },
        "audioFrecuency" : RATE
    }

    #TODO: Implementar los datos y el fourier. Guardarlos en un diccionario.
    atm.save(data,archivo,os.getcwd(),nombreDeArchivo)


def pausar():
    shared_data.lock.acquire()
    shared_data.pausado = not shared_data.pausado  # Cambiar el estado de pausado

    if shared_data.pausado:
        # Detener el proceso de cuenta mientras está en pausa
        time.after_cancel(shared_data.proceso)
    else:
        # Reanudar el proceso de cuenta cuando se reanuda la grabación
        cuenta()
    shared_data.lock.release()

def salir():
    ventana.quit()

def guardarWAV():
    ventana.quit()

# CONTADOR DE TIEMPO
time = Label(ventana, fg='green', width=20, text="0:00:00", bg="black", font=("","30"))
time.place(x=10,y=20)
ventana.geometry("1000x500")

# BOTONES 
btnIniciar = Button(ventana, fg='blue', width=5, text='Grabar', command=iniciar)
btnIniciar.place(x=122, y=71)
btnParar = Button(ventana, fg='blue', width=5, text='Parar', command=parar)
btnParar.place(x=244, y=71)
btnDir = Button(ventana, text="Carpeta", width=5, command=direc)
btnDir.place(x=0, y=71)
btnAbrir = Button(ventana, text="Abrir", width=5, command=abrir)
btnAbrir.place(x=366, y=71)

# Boton para pausar
btnPausar = Button(ventana, fg='blue', width=5, text='Pausar', command=pausar)
btnPausar.place(x=190, y=71)

#Boton para salir
btnSalir = Button(ventana, width=5, text="Salir", command=salir)
btnSalir.place(x=122, y=91)

#Boton para salir
btnGuardarWAV = Button(ventana, width=5, text="WAV", command=guardarWAV)
btnGuardarWAV.place(x=244, y=91)

etDir = Entry(ventana, width=77, bg="lavender", textvariable=shared_data.directorio_actual)
etDir.place(x=10, y=0)

dire()

ventana.mainloop()
