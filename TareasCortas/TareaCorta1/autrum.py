import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import pyaudio
import wave
import threading
import os
from tkinter import StringVar, Label, Entry, messagebox

class InterfazApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Autrum")

        # Variables de control para la grabación y reproducción de audio
        self.directorio_actual = StringVar()
        self.grabando = False
        self.reproduciendo = False
        self.pausado = False
        self.CHUNK = 1024
        self.data = ""
        self.stream = None
        self.audio = pyaudio.PyAudio()
        self.f = None

        # Crear los graficos
        self.fig_1 = plt.Figure(figsize=(5, 3), dpi=100)
        self.canvas_1 = FigureCanvasTkAgg(self.fig_1, master=self.root)
        self.canvas_1_widget = self.canvas_1.get_tk_widget()
        self.canvas_1_widget.grid(row=0, column=0, columnspan=2)

        self.fig_2 = plt.Figure(figsize=(5, 3), dpi=100)
        self.canvas_2 = FigureCanvasTkAgg(self.fig_2, master=self.root)
        self.canvas_2_widget = self.canvas_2.get_tk_widget()
        self.canvas_2_widget.grid(row=0, column=2, columnspan=2)

        # CONTADOR DE TIEMPO
        self.time = Label(self.root, fg='green', width=20, text="0:00:00", bg="black", font=("", "30"))
        self.time.grid(row=4, column=0)
        self.root.geometry("488x97")

        # BOTONES
        self.btnIniciar = ttk.Button(self.root, text='Grabar', command=self.iniciar_grabadora)
        self.btnParar = ttk.Button(self.root, text='Parar', command=self.parar)
        self.btnDir = ttk.Button(self.root, text="Carpeta", command=self.direc)
        self.btnAbrir = ttk.Button(self.root, text="Abrir", command=self.abrir)
        self.btnPausar = ttk.Button(self.root, text='Pausar', command=self.pausar)

        self.etDir = Entry(self.root, width=77, bg="lavender", textvariable=self.directorio_actual)

        self.dire()

        # BOTONES DEL PRIMER CÓDIGO
        self.btn_continuar = ttk.Button(self.root, text="Continuar", command=self.mostrar_grafico1)
        self.btn_pausar_1 = ttk.Button(self.root, text="Pausa", command=self.salir)
        self.btn_analizar = ttk.Button(self.root, text="Continuar", command=self.mostrar_grafico2)
        self.btn_pausar_2 = ttk.Button(self.root, text="Pausa", command=self.salir)

        # Posicionar elementos en la ventana utilizando grid
        self.canvas_1_widget.grid(row=0, column=0, columnspan=2)
        self.canvas_2_widget.grid(row=0, column=2, columnspan=2)
        self.btn_continuar.grid(row=1, column=0)
        self.btn_pausar_1.grid(row=1, column=1)
        self.btn_analizar.grid(row=1, column=2)
        self.btn_pausar_2.grid(row=1, column=3)
        self.btnIniciar.grid(row=2, column=0)
        self.btnParar.grid(row=2, column=1)
        self.btnDir.grid(row=2, column=2)
        self.btnAbrir.grid(row=2, column=3)
        self.btnPausar.grid(row=2, column=4)
        self.etDir.grid(row=3, column=0)

        # Iniciar el proceso de actualización de datos
        self.x1_values = [1, 2, 3, 4, 5]
        self.y1_values = [15, 30, 5, 10, 30]
        self.x2_values = [1, 2, 3, 4, 5]
        self.y2_values = [10, 5, 20, 15, 30]

        # Iniciar el proceso de actualización de datos
        self.actualizar_datos1()
        self.actualizar_datos2()

        # Iniciar la grabadora
        self.iniciar_grabadora()

    def mostrar_grafico1(self):
        self.fig_1.clf()  # Limpia el gráfico anterior
        dibujo = self.fig_1.add_subplot(111)
        dibujo.plot(self.x1_values, self.y1_values, marker='o')
        dibujo.set_title("Gráfico 1")
        dibujo.set_xticks([])  # Oculta las etiquetas en el eje x
        dibujo.set_yticks([])  # Oculta las etiquetas en el eje y
        self.canvas_1.draw()

    def mostrar_grafico2(self):
        self.fig_2.clf()  # Limpia el gráfico anterior
        dibujo = self.fig_2.add_subplot(111)
        dibujo.plot(self.x2_values, self.y2_values, marker='o')
        dibujo.set_title("Gráfico 2")
        dibujo.set_xticks([])  # Oculta las etiquetas en el eje x
        dibujo.set_yticks([])  # Oculta las etiquetas en el eje y
        self.canvas_2.draw()

    def actualizar_datos1(self):
        self.x1_values.append(self.x1_values[-1] + 1)
        self.y1_values.append(random.randint(0, 100))
        if len(self.x1_values) > 10:
            self.x1_values.pop(0)
            self.y1_values.pop(0)
        self.mostrar_grafico1()
        self.root.after(1000, self.actualizar_datos1)

    def actualizar_datos2(self):
        self.x2_values.append(self.x2_values[-1] + 1)
        self.y2_values.append(random.randint(0, 100))
        if len(self.x2_values) > 10:
            self.x2_values.pop(0)
            self.y2_values.pop(0)
        self.mostrar_grafico2()
        self.root.after(1000, self.actualizar_datos2)

    def iniciar_grabadora(self):
        # Verificar si ya está grabando
        if self.grabando:
            return

        # Configurar los parámetros de grabación de audio
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        archivo = "grabacion.wav"  # Nombre del archivo de grabación

        # Crear un flujo de audio para la grabación
        self.stream = self.audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )

        # Iniciar la grabación
        self.frames = []  # Aquí se almacenarán los frames de audio
        self.grabando = True

        # Iniciar un hilo para la grabación
        self.hilo_grabacion = threading.Thread(
            target=self.grabar_audio,
            args=(archivo,)
        )
        self.hilo_grabacion.start()

        # Actualizar la interfaz, deshabilitar el botón de inicio, habilitar el de detener
        self.bloqueo("disabled")

    def grabar_audio(self, archivo):
        while self.grabando:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)

        # Detener la grabación
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        # Guardar los frames grabados en un archivo WAV
        wf = wave.open(archivo, 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        # Actualizar la interfaz, habilitar el botón de inicio, deshabilitar el de detener
        self.bloqueo("normal")
        self.grabando = False

    def abrir(self):
        # Limpiar contadores y variables relacionadas con la grabación
        self.clear_contador()

        # Crear una instancia de PyAudio
        audio = pyaudio.PyAudio()

        # Mostrar el cuadro de diálogo de selección de archivos
        open_archive = filedialog.askopenfilename(
            initialdir="/",
            title="Seleccione archivo",
            filetypes=(("Archivos MP3", "*.mp3"), ("Todos los archivos", "*.*"))
        )

        if open_archive != "":
            try:
                # Establecer que se está reproduciendo
                self.reproduciendo = True

                # Abrir el archivo de audio en modo lectura
                self.f = wave.open(open_archive, "rb")

                # Configurar el flujo de audio para la reproducción
                self.stream = audio.open(
                    format=audio.get_format_from_width(self.f.getsampwidth()),
                    channels=self.f.getnchannels(),
                    rate=self.f.getframerate(),
                    output=True
                )

                # Leer los frames del archivo de audio
                self.data = self.f.readframes(self.CHUNK)

                # Deshabilitar botones mientras se reproduce
                self.bloqueo('disabled')

                # Iniciar hilos para contar el tiempo y reproducir el audio
                t = threading.Thread(target=self.cuenta)
                t.start()
                t2 = threading.Thread(target=self.reproduce)
                t2.start()

            except Exception as e:
                # Mostrar mensaje de error si no se puede abrir el archivo
                messagebox.showwarning("ERROR", f"No se pudo abrir el archivo especificado:\n{str(e)}")
                self.reproduciendo = False

    def parar(self):
        if self.grabando:
            self.grabando = False
            self.time.after_cancel(self.proceso)
            self.clear_contador()
        elif self.reproduciendo:
            self.reproduciendo = False
        # Habilitar botones nuevamente (puedes descomentar esta línea)
        # self.bloqueo('normal')

    def direc(self):
        directorio = filedialog.askdirectory()
        if directorio != "":
            os.chdir(directorio)
            self.dire()

    def pausar(self):
        self.pausado = not self.pausado  # Cambiar el estado de pausado

        if self.pausado:
            # Detener el proceso de cuenta mientras está en pausa
            self.time.after_cancel(self.proceso)
        else:
            # Reanudar el proceso de cuenta cuando se reanuda la grabación
            self.cuenta()

    def salir(self):
        self.root.quit()

    def formato(self, c):
        if c < 10:
            c = "0" + str(c)
        return c

    def cuenta(self):
        self.time_text = str(self.contador1) + ":" + self.formato(self.contador2) + ":" + self.formato(self.contador)
        self.contador += 1
        if self.contador == 60:
            self.contador = 0
            self.contador2 += 1
        if self.contador2 == 60:
            self.contador2 = 0
            self.contador1 += 1
        self.time['text'] = self.time_text
        self.proceso = self.root.after(1000, self.cuenta)

    def bloqueo(self, s):
        self.btn_continuar.config(state=s)
        self.btn_pausar_1.config(state=s)
        self.btn_analizar.config(state=s)
        self.btn_pausar_2.config(state=s)
        self.btnIniciar.config(state=s)
        self.btnParar.config(state=s)
        self.btnDir.config(state=s)
        self.btnAbrir.config(state=s)
        self.btnPausar.config(state=s)

    def dire(self):
        self.directorio_actual.set(os.getcwd())

    def grabacion(self):
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        CHUNK = self.CHUNK
        frames = []

        stream = self.audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

        while self.grabando:
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        self.audio.terminate()

        # Guardar el archivo de audio grabado (ejemplo: "grabacion.wav")
        archivo = "grabacion.wav"
        wf = wave.open(archivo, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    def reproduce(self):
        if self.reproduciendo:
            return

        self.reproduciendo = True
        open_archive = filedialog.askopenfilename(initialdir="/",
                                                title="Seleccione archivo",
                                                filetypes=(("WAV files", "*.wav"), ("all files", "*.*")))

        if open_archive != "":
            try:
                wf = wave.open(open_archive, "rb")
                stream = self.audio.open(format=self.audio.get_format_from_width(wf.getsampwidth()),
                                        channels=wf.getnchannels(),
                                        rate=wf.getframerate(),
                                        output=True)

                data = wf.readframes(self.CHUNK)
                self.bloqueo('disabled')

                while data and self.reproduciendo:
                    stream.write(data)
                    data = wf.readframes(self.CHUNK)

                stream.stop_stream()
                stream.close()
                wf.close()

                self.bloqueo('normal')
                self.reproduciendo = False

            except Exception as e:
                messagebox.showwarning("ERROR", f"No se pudo abrir el archivo especificado: {str(e)}")
                self.reproduciendo = False

    def clear_contador(self):
        self.contador1 = 0
        self.contador2 = 0
        self.contador = 0
        self.time_text = "0:00:00"
        self.time['text'] = self.time_text
        if hasattr(self, 'proceso'):
            self.root.after_cancel(self.proceso)

root = tk.Tk()
app = InterfazApp(root)
root.mainloop()

