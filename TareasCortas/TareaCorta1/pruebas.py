import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def mostrar_grafico_1():
    fig_1.clf()  # Limpia el gráfico anterior
    ax = fig_1.add_subplot(111)
    ax.plot([1, 2, 3, 4], [10, 5, 20, 15], marker='o')
    ax.set_title("Gráfico 1")
    canvas_1.draw()

def mostrar_grafico_2():
    fig_2.clf()  # Limpia el gráfico anterior
    ax = fig_2.add_subplot(111)
    ax.bar(['A', 'B', 'C', 'D'], [25, 10, 35, 20])
    ax.set_title("Gráfico 2")
    canvas_2.draw()

def salir():
    root.quit()

root = tk.Tk()
root.title("Interfaz Gráfica")

# Crear botones
btn_grafico1 = ttk.Button(root, text="Mostrar Gráfico 1", command=mostrar_grafico_1)
btn_grafico2 = ttk.Button(root, text="Mostrar Gráfico 2", command=mostrar_grafico_2)
btn_salir = ttk.Button(root, text="Salir", command=salir)

# Crear espacios para los gráficos
fig_1 = plt.Figure()
canvas_1 = FigureCanvasTkAgg(fig_1, master=root)
canvas_1_widget = canvas_1.get_tk_widget()
canvas_1_widget.configure(width=400, height=300)

fig_2 = plt.Figure()
canvas_2 = FigureCanvasTkAgg(fig_2, master=root)
canvas_2_widget = canvas_2.get_tk_widget()
canvas_2_widget.configure(width=400, height=300)

# Posicionar elementos en la ventana
btn_grafico1.pack()
btn_grafico2.pack()
canvas_1_widget.pack()
canvas_2_widget.pack()
btn_salir.pack()

root.mainloop()