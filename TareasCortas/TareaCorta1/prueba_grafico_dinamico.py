import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

def mostrar_grafico():
    plt.clf()  # Limpia el gráfico anterior
    ax = fig.add_subplot(111)
    ax.plot(x_values, y_values, marker='o')
    ax.set_title("Gráfico Dinámico")
    ax.set_xticks([])  # Oculta las etiquetas en el eje x
    ax.set_yticks([])  # Oculta las etiquetas en el eje y
    canvas.draw()

def actualizar_datos():
    global x_values, y_values
    x_values.append(x_values[-1] + 1)
    y_values.append(random.randint(0, 100))
    if len(x_values) > 10:  # Limitar el número de puntos en el gráfico
        x_values.pop(0)
        y_values.pop(0)
    mostrar_grafico()
    root.after(1000, actualizar_datos)  # Llamar a la función nuevamente después de 1 segundo

def salir():
    root.quit()

root = tk.Tk()
root.title("Interfaz Gráfica Dinámica")

# Crear botón y espacio para el gráfico
btn_mostrar = ttk.Button(root, text="Mostrar Gráfico", command=mostrar_grafico)
btn_salir = ttk.Button(root, text="Salir", command=salir)

fig = plt.Figure()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()

# Posicionar elementos en la ventana
btn_mostrar.pack()
canvas_widget.pack()
btn_salir.pack()

x_values = [1, 2, 3, 4, 5]
y_values = [10, 5, 20, 15, 30]

actualizar_datos()  # Iniciar el proceso de actualización de datos

root.mainloop()
