#!/usr/bin/env python3

import cv2
import numpy as np
import pyautogui as pg
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def rgb_to_hsl(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    mx = max(r, g, b)
    mn = min(r, g, b)
    l = (mx + mn) / 2
    if mx == mn:
        h = s = 0
    else:
        d = mx - mn
        s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
        if mx == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif mx == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        h /= 6
    return f'H: {int(h*360)} S: {int(s*100)} L: {int(l*100)}'

def copiar_formato(valor):
    root.clipboard_clear()
    root.clipboard_append(valor)
    root.update()
    print(f'Valor copiado al portapapeles: {valor}')

def capturarPunto(event=None):
    # Coordenadas del cursor
    position = pg.position()

    # Captura del área
    screenshot = pg.screenshot(region=(position[0]-1, position[1]-1, 1, 1))

    # Convierte la imagen a RGB
    im = screenshot.convert('RGB')

    # Obtiene el color del píxel en la posición (0, 0) de la región capturada
    color = im.getpixel((0, 0))

    # Mostrar los valores RGB en el Label
    rgb_values.set(f'R: {color[0]} \nG: {color[1]} \nB: {color[2]}')

    # Colocar los valores RGB en el Entry para copiarlos
    entry_rgb.delete(0, tk.END)
    entry_rgb.insert(0, f'{color[0]} {color[1]} {color[2]}')

    hex_color = rgb_to_hex(color)
    entry_hex.delete(0, tk.END)
    entry_hex.insert(0, hex_color)

    hsl_color = rgb_to_hsl(color)
    entry_hsl.delete(0, tk.END)
    entry_hsl.insert(0, hsl_color)

    # Cambia el fondo de la ventana al color capturado
    frameTop.config(background=hex_color)

    return color

# Función para actualizar la imagen en el Label de Tkinter
def update_image():
    # Tamaño del área que se mostrará
    size = 15
    position = pg.position()
    screenshot = pg.screenshot(region=(int(position[0]-size/2), int(position[1]-size/2), size, size))

    # Convierte el array de la captura a BGR
    im = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Amplía el área del cursor
    im = cv2.resize(im, (size*10, size*10), interpolation=cv2.INTER_AREA)

    # Rectángulo en el centro de la imagen
    startingC = int((size*10)/2 - 5)
    endingC = int((size*10)/2 + 5)
    im = cv2.rectangle(im, (startingC, startingC), (endingC, endingC), (0,0,0), 3)

    # Convertir la imagen a un formato que Tkinter pueda usar
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(im)
    imgtk = ImageTk.PhotoImage(image=im_pil)

    # Actualiza la imagen en el Label
    label.config(image=imgtk)
    label.image = imgtk

    # Se llama a sí misma cada 10 ms
    root.after(10, update_image)


# Ventana principal
root = tk.Tk()
root.geometry("350x450")
root.title("Cuentagotas")
root.iconbitmap("favicon.ico")

# Frame superior
frameTop = tk.Frame(root)
frameTop.pack(side="top", fill="both", expand=True)
frameTop.pack_propagate(False)  # Evita que el frame cambie de tamaño

# Frame contenedor para centrar vertical y horizontalmente
frameTop_center = tk.Frame(frameTop)
frameTop_center.pack(expand=True, anchor="center")

# Label de la imagen
label = ttk.Label(frameTop_center)
label.pack(pady=15)

# Instrucciones
label_font = ("Helvetica", 10, "bold")
label_instruction = ttk.Label(frameTop_center, text='Presiona ESPACIO para capturar', foreground="white", background="black", anchor="center", font=label_font)
label_instruction.pack(ipadx=5, ipady=10, padx=5)

# Recuadro para mostrar el color elegido
color_box = tk.Frame(
    frameTop_center,
    width=80,
    height=40,
    bg="#ffffff",
    highlightbackground="#888888",  # Color del borde
    highlightthickness=2
)
color_box.pack(pady=10)
color_box.pack_propagate(False)  # Mantiene el tamaño fijo

# Frame inferior
frameBottom = ttk.Frame(root, height=130)
frameBottom.pack_propagate(False)  # Evita que el frame cambie de tamaño
frameBottom.pack(side="top", fill="both")

def crear_fila_formato(parent, titulo, variable_entry):
    fila = ttk.Frame(parent)
    fila.pack(pady=4, side="top", anchor="center")
    label = ttk.Label(fila, text=titulo, width=6, anchor="center")
    label.pack(side="left", padx=2)
    entry = ttk.Entry(fila, textvariable=variable_entry if variable_entry else None, justify='center', width=22)
    entry.pack(side="left", padx=2)
    btn = ttk.Button(fila, text="📋", width=2, command=lambda: copiar_formato(entry.get()))
    btn.pack(side="left", padx=2)
    return entry

# Variables para los valores
var_rgb = tk.StringVar()
var_hex = tk.StringVar()
var_hsl = tk.StringVar()

# RGB
entry_rgb = crear_fila_formato(frameBottom, "RGB", var_rgb)
# HEX
entry_hex = crear_fila_formato(frameBottom, "HEX", var_hex)
# HSL
entry_hsl = crear_fila_formato(frameBottom, "HSL", var_hsl)

# Actualiza los valores de los StringVar y Entry en capturarPunto
def capturarPunto(event=None):
    position = pg.position()
    screenshot = pg.screenshot(region=(position[0]-1, position[1]-1, 1, 1))
    im = screenshot.convert('RGB')
    color = im.getpixel((0, 0))

    var_rgb.set(f'{color[0]} {color[1]} {color[2]}')
    var_hex.set(rgb_to_hex(color))
    var_hsl.set(rgb_to_hsl(color))
    color_box.config(bg=rgb_to_hex(color))
    return color

# Espacio para capturar el punto
root.bind('<space>', capturarPunto)

# Inicia la actualización de la imagen
update_image()

root.mainloop()
print("Programa finalizado")