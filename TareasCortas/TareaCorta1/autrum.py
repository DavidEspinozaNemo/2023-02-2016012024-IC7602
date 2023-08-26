import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

def mostrar_grafico1():
    plt.clf()  # Limpia el gráfico anterior
    dibujo = fig_1.add_subplot(111)
    dibujo.plot(x1_values, y1_values, marker='o')
    dibujo.set_title("Gráfico 1")
    dibujo.set_xticks([])  # Oculta las etiquetas en el eje x
    dibujo.set_yticks([])  # Oculta las etiquetas en el eje y
    canvas_1.draw()

def mostrar_grafico2():
    plt.clf()  # Limpia el gráfico anterior
    dibujo = fig_2.add_subplot(111)
    dibujo.plot(x2_values, y2_values, marker='o')
    dibujo.set_title("Gráfico 2")
    dibujo.set_xticks([])  # Oculta las etiquetas en el eje x
    dibujo.set_yticks([])  # Oculta las etiquetas en el eje y
    canvas_2.draw()

def actualizar_datos1():
    global x1_values, y1_values
    x1_values.append(x1_values[-1] + 1)
    y1_values.append(random.randint(0, 100))
    # arriba se añaden los valores
    if len(x1_values) > 10:  # Limitar el número de puntos en el gráfico
        x1_values.pop(0)
        y1_values.pop(0)
    mostrar_grafico1()
    root.after(1000, actualizar_datos1)  # Llamar a la función nuevamente después de 1 segundo

def actualizar_datos2():
    global x2_values, y2_values
    x2_values.append(x2_values[-1] + 1)
    y2_values.append(random.randint(0, 100))
    # arriba se añaden los valores
    if len(x2_values) > 10:  # Limitar el número de puntos en el gráfico
        x2_values.pop(0)
        y2_values.pop(0)
    mostrar_grafico2()
    root.after(1000, actualizar_datos2)  # Llamar a la función nuevamente después de 1 segundo

def salir():
    root.quit()

root = tk.Tk()
root.title("Autrum")

# Crear los botones
btn_continuar  = ttk.Button(root, text="Continuar", command=mostrar_grafico1)
btn_pausar     = ttk.Button(root, text="Pausa", command=salir)
btn_analizar   = ttk.Button(root, text="Continuar", command=mostrar_grafico2)
btn_reproducir = ttk.Button(root, text="Pausa", command=salir)

# Habilitar los espacios de los graficos
fig_1 = plt.Figure()
canvas_1 = FigureCanvasTkAgg(fig_1, master=root)
canvas_1_widget = canvas_1.get_tk_widget()
canvas_1_widget.configure(width=500, height=300)

fig_2 = plt.Figure()
canvas_2 = FigureCanvasTkAgg(fig_2, master=root)
canvas_2_widget = canvas_2.get_tk_widget()
canvas_2_widget.configure(width=500, height=300)

# Posicionar elementos en la ventana utilizando grid
canvas_1_widget.grid(row=0, column=0, columnspan=2)
canvas_2_widget.grid(row=0, column=2, columnspan=2)
btn_continuar.grid(row=1, column=0)
btn_pausar.grid(row=1, column=1)
btn_analizar.grid(row=1, column=2)
btn_reproducir.grid(row=1, column=3)


# valores de prueba

x1_values = [1, 2, 3, 4, 5]
y1_values = [15, 30, 5, 10, 30]

x2_values = [1, 2, 3, 4, 5]
y2_values = [10, 5, 20, 15, 30]

actualizar_datos2()  # Iniciar el proceso de actualización de datos
actualizar_datos1()
# inicialización del programa

root.mainloop()