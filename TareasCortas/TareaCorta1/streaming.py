# Este código se encuentra basado en los códigos de la siguiente página: https://programacionpython80889555.wordpress.com/2018/10/16/grabacion-de-sonido-con-pyaudio-ejercicio-basico-en-python/


"""Aquí se importan las bibliotecas necesarias. Tkinter se utiliza para la interfaz gráfica, pyaudio para manejar el audio, 
   os para operaciones en directorios, wave para trabajar con archivos de audio WAV, threading para la ejecución concurrente 
   de funciones y glob para buscar archivos que coincidan con un patrón."""

from tkinter import Tk,Label,Button,filedialog,Entry,StringVar,messagebox
import glob
import pyaudio
import os
import wave
import threading
import atm

#Esta función restablece los contadores de tiempo contador, contador1 y contador2.
def clear_contador():
    global contador,contador1,contador2
    contador=0
    contador1=0
    contador2=0

# La función dire establece el valor de la variable directorio_actual (directorio actual) de tipo StringVar en el directorio 
# de trabajo actual obtenido de os.getcwd().
def dire():
    directorio_actual.set(os.getcwd())

"""La función iniciar se llama cuando se presiona el botón "Grabar". Configura el proceso de grabación de audio. Inicializa 
   un objeto PyAudio y establece grabando en True para indicar que la grabación está activa. También deshabilita los botones 
   mediante la función bloqueo y comienza varios hilos para manejar la grabación y el conteo de tiempo."""
def iniciar():
    global grabando
    global proceso
    global act_proceso
    clear_contador()
    audio=pyaudio.PyAudio()
    bloqueo('disabled')
    grabando=True
    FORMAT=pyaudio.paInt16
    CHANNELS=2
    RATE=44100
    act_proceso=True
    archivo="grabacion.mp3"
    t1=threading.Thread(target=grabacion, args=(FORMAT,CHANNELS,RATE,CHUNK,audio,archivo))
    t=threading.Thread(target=cuenta)
    t1.start()
    t.start()

# Esta función toma un número c y lo devuelve con un cero inicial si es menor que 10. Se utiliza para formatear los minutos y
# segundos.
def formato(c):
    if c<10:
        c="0"+str(c)
    return c

"""La función cuenta actualiza la pantalla del temporizador mientras se graba o reproduce el audio. Actualiza la etiqueta con 
   el valor de tiempo actual basado en contador, contador1 y contador2"""
def cuenta():
    global proceso
    global contador,contador1,contador2
    time['text'] = str(contador1)+":"+str(formato(contador2))+":"+str(formato(contador))
    contador+=1
    if contador==60:
        contador=0
        contador2+=1
    if contador2==60:
        contador2=0
        contador1+=1
    proceso=time.after(1000, cuenta)

"""La función abrir se llama cuando se presiona el botón "Abrir". Permite al usuario seleccionar un archivo MP3 para
   reproducirlo. Inicializa la reproducción de audio y maneja el inicio de un hilo tanto para contar el tiempo como para 
   reproducir el audio."""
def abrir():
    global data
    global stream
    global f
    global reproduciendo
    clear_contador()
    audio=pyaudio.PyAudio()
    open_archive=filedialog.askopenfilename(initialdir = "/",
                 title = "Seleccione archivo",filetypes = (("mp3 files","*.mp3"),
                 ("all files","*.*")))
    if open_archive!="":
        try:
            reproduciendo=True
            f = wave.open(open_archive,"rb")
            stream = audio.open(format = audio.get_format_from_width(f.getsampwidth()),  
                        channels = f.getnchannels(),  
                        rate = f.getframerate(),
                        output = True)
            data = f.readframes(CHUNK)
            bloqueo('disabled')
            t=threading.Thread(target=cuenta)
            t.start()
            t2=threading.Thread(target=reproduce)
            t2.start()
        except:
            messagebox.showwarning("ERROR","No se pudo abrir al archivo especificado")
            reproduciendo=False
"""La función reproduce se encarga de reproducir el archivo de audio seleccionado. Escribe continuamente datos de audio 
   en el flujo de salida hasta que se haya reproducido todo el archivo."""
def reproduce():
    global data
    global stream
    global f
    
    while data and reproduciendo==True:  
        stream.write(data)  
        data = f.readframes(CHUNK)  
 
    stream.stop_stream()  
    stream.close()  
 
    audio.terminate()
    time.after_cancel(proceso)
    #print("FIN")
    bloqueo('normal')

"""La función bloqueo habilita o deshabilita los botones especificados cambiando su atributo state. Se utiliza para 
   controlar el comportamiento de los botones durante la grabación y la reproducción."""
def bloqueo(s):
    btnIniciar.config(state=s)
    btnDir.config(state=s)
    btnAbrir.config(state=s)

"""La función parar se llama cuando se presiona el botón "Parar". Detiene la grabación o la reproducción y restaura 
   la funcionalidad de los botones."""    
def parar():
    global grabando
    global reproduciendo
    if grabando==True:
        grabando=False
        time.after_cancel(proceso)
        clear_contador()
    elif reproduciendo==True:
        reproduciendo=False
    bloqueo('normal')

"""La función direc se activa cuando se presiona el botón "Carpeta". Abre un cuadro de diálogo de carpeta para
   permitir al usuario elegir un directorio. Si se selecciona un directorio, cambia el directorio de trabajo actual y 
   actualiza la visualización del directorio utilizando la función dire."""
def direc():
    directorio=filedialog.askdirectory()
    if directorio!="":
        os.chdir(directorio)
        dire()

"""La función grabacion se encarga del proceso de grabación de audio. Abre un flujo, lee datos de audio en fragmentos
   y agrega los datos a frames hasta que se detenga la grabación. Luego, guarda el audio grabado en un archivo MP3"""
def grabacion(FORMAT, CHANNELS, RATE, CHUNK, audio, archivo):
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []

    while grabando == True:
        if not pausado:
            data = stream.read(CHUNK)
            frames.append(data)
        else:
            # Agregar algún tipo de pausa aquí, si deseas
            pass

    # DETENEMOS GRABACIÓN
    stream.stop_stream()
    stream.close()
    audio.terminate()

    grabs = glob.glob('*.mp3')

    # CREAR/GUARDAR EL ARCHIVO DE AUDIO
    count = 0
    for i in grabs:
        if "grabacion" in i:
            count += 1
    if count > 0:
        archivo = "grabacion" + "(" + str(count) + ")" + ".mp3"

    waveFile = wave.open(archivo, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()



def pausar():
    global pausado
    pausado = not pausado  # Cambiar el estado de pausado

    if pausado:
        # Detener el proceso de cuenta mientras está en pausa
        time.after_cancel(proceso)
    else:
        # Reanudar el proceso de cuenta cuando se reanuda la grabación
        cuenta()



"""configura la ventana de la GUI utilizando Tkinter, inicializa las variables necesarias, crea botones, etiquetas y 
   la visualización del directorio actual, y comienza el bucle de eventos principal con ventana.mainloop()"""
   
#CREAR VENTANA
ventana = Tk()
ventana.title('Grabadora Audio mp3')

#VARIABLES INICIALES
directorio_actual=StringVar()
grabando=False
reproduciendo=False
pausado = False
CHUNK=1024
data=""
stream=""
audio=pyaudio.PyAudio() 
f=""

#CONTADOR DE TIEMPO
time = Label(ventana, fg='green', width=20, text="0:00:00", bg="black", font=("","30"))
time.place(x=10,y=20)
ventana.geometry("488x97")

#BOTONES 
btnIniciar=Button(ventana, fg='blue',width=5, text='Grabar', command=iniciar)
btnIniciar.place(x=122,y=71)
btnParar=Button(ventana, fg='blue', width=5, text='Parar', command=parar)
btnParar.place(x=244,y=71)
btnDir=Button(ventana, text="Carpeta",width=5,command=direc)
btnDir.place(x=0,y=71)
btnAbrir=Button(ventana, text="Abrir",width=5,command=abrir)
btnAbrir.place(x=366,y=71)


#Boton para pausar
btnPausar = Button(ventana, fg='blue', width=5, text='Pausar', command=pausar)
btnPausar.place(x=190, y=71)

etDir=Entry(ventana,width=77,bg="lavender",textvariable=directorio_actual)
etDir.place(x=10,y=0)

dire()
 
ventana.mainloop()