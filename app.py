#!/usr/bin/env python3

import cv2
import numpy as np
import pyautogui as pg
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import darkdetect


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

def copiar_formato(valor, boton=None):
    root.clipboard_clear()
    root.clipboard_append(valor)
    root.update()
    print(f'Valor copiado al portapapeles: {valor}')
    mensaje_copiado.config(text="¡Valor copiado!")
    mensaje_copiado.after(1200, lambda: mensaje_copiado.config(text=""))

def capturarPunto(event=None):
    # Coordenadas del cursor
    position = pg.position()

    # Captura del área
    screenshot = pg.screenshot(region=(position[0]-1, position[1]-1, 1, 1))

    # Convierte la imagen a RGB
    im = screenshot.convert('RGB')

    # Obtiene el color del píxel en la posición (0, 0) de la región capturada
    color = im.getpixel((0, 0))

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


# Detectar modo oscuro o claro
if darkdetect.isDark():
    BG_COLOR = "#23272e"
    FG_COLOR = "#f7f7f7"
    ENTRY_BG = "#2d323a"
    ENTRY_FG = "#f7f7f7"
    BOX_BG = "#23272e"
    BOX_BORDER = "#444"
    BTN_BG = "#23272e"
    BTN_FG = "#f7f7f7"
    INSTR_BG = "#2d323a"
    INSTR_FG = "#eaeaea"
else:
    BG_COLOR = "#f7f7f7"
    FG_COLOR = "#23272e"
    ENTRY_BG = "#ffffff"
    ENTRY_FG = "#23272e"
    BOX_BG = "#ffffff"
    BOX_BORDER = "#bbbbbb"
    BTN_BG = "#f7f7f7"
    BTN_FG = "#23272e"
    INSTR_BG = "#eaeaea"
    INSTR_FG = "#444"

# Ventana principal
root = tk.Tk()
root.geometry("320x400")
root.title("Cuentagotas")
root.iconbitmap("favicon.ico")
root.configure(bg=BG_COLOR)

# Configuración de grid para diseño dinámico
root.rowconfigure(0, weight=2)
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)

# Frame superior minimalista
frameTop = tk.Frame(root, bg=BG_COLOR)
frameTop.grid(row=0, column=0, sticky="nsew")

frameTop_center = tk.Frame(frameTop, bg=BG_COLOR)
frameTop_center.pack(expand=True, anchor="center")

# Label de la imagen (sin borde, más pequeño)
label = ttk.Label(frameTop_center)
label.pack(pady=(18, 8))

# Instrucciones minimalistas
label_font = ("Segoe UI", 10, "normal")
label_instruction = ttk.Label(
    frameTop_center,
    text='Presiona ESPACIO para capturar',
    foreground=INSTR_FG,
    background=INSTR_BG,
    anchor="center",
    font=label_font,
    padding=(8, 6)
)
label_instruction.pack(pady=(0, 10))

# Recuadro de color minimalista
color_box = tk.Frame(
    frameTop_center,
    width=60,
    height=32,
    bg=BOX_BG,
    highlightbackground=BOX_BORDER,
    highlightthickness=1,
    bd=0,
    relief="flat"
)
color_box.pack(pady=(0, 8))
color_box.pack_propagate(False)

# Frame inferior minimalista
frameBottom = tk.Frame(root, bg=BG_COLOR)
frameBottom.grid(row=1, column=0, sticky="nsew")

# Fila de formato minimalista
style = ttk.Style()
style.configure("Minimal.TEntry", font=("Segoe UI", 10), padding=2, relief="flat", fieldbackground=ENTRY_BG, foreground=ENTRY_FG)
style.configure("Minimal.TLabel", font=("Segoe UI", 9), background=BG_COLOR, foreground=FG_COLOR)
style.configure("Minimal.TButton", font=("Segoe UI", 10), padding=0, relief="flat", background=BTN_BG, foreground=BTN_FG)

def crear_fila_formato(parent, titulo, variable_entry):
    fila = tk.Frame(parent, bg=BG_COLOR)
    fila.pack(pady=6, anchor="center")
    label = ttk.Label(fila, text=titulo, width=5, anchor="center", style="Minimal.TLabel")
    label.pack(side="left", padx=(0, 4))
    entry = tk.Entry(
        fila,
        textvariable=variable_entry if variable_entry else None,
        justify='center',
        width=18,
        fg=ENTRY_FG,
        bg=ENTRY_BG,
        relief="flat",
        font=("Segoe UI", 10)
    )
    entry.pack(side="left", padx=(0, 4))
    btn = tk.Button(
        fila,
        text="📋",
        width=2,
        fg=BTN_FG,
        bg=BTN_BG,
        relief="flat",
        font=("Segoe UI", 10),
        activebackground=BOX_BORDER,
        activeforeground=FG_COLOR,
        command=lambda: copiar_formato(entry.get(), btn)
    )
    btn.pack(side="left")
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

# Mensaje de copiado
mensaje_copiado = tk.Label(frameBottom, text="", fg="#4caf50", bg=BG_COLOR, font=("Segoe UI", 9, "bold"))
mensaje_copiado.pack(pady=(0, 6))

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