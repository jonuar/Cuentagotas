# Cuentagotas

Script que toma el valor RGB, HEX y HSL de un pixel en la pantalla.

## Características
- Muestra el color bajo el cursor en tiempo real.
- Permite capturar el color con la tecla ESPACIO.
- Visualiza el color elegido en un recuadro con borde.
- Historial interactivo de los últimos 5 colores elegidos.
- Al hacer clic en un color del historial, se rellenan los campos con ese color.
- Copia fácilmente los valores RGB, HEX y HSL al portapapeles con un botón.
- Muestra un mensaje temporal al copiar.
- Los valores copiados están listos para usar en CSS/HTML: `rgb(r, g, b)`, `#hex`, `hsl(h, s%, l%)`.
- Ajusta los estilos de Tkinter dependiendo de la hora o configuración del sistema

## Requisitos
- Python 3.x
- [requirements.txt](requirements.txt) (instalar con `pip install -r requirements.txt`)

## Uso
1. Ejecuta el script:
   ```bash
   python app.py
   ```
2. Mueve el cursor sobre cualquier parte de la pantalla.
3. Presiona ESPACIO para capturar el color.
4. Usa los botones 📋 para copiar el valor en el formato deseado.
5. Haz clic en un color del historial para reutilizarlo.

