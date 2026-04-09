import tkinter as tk
import requests

historial = []

try:
    with open("historial.txt", "r") as archivo:
        for linea in archivo:
            historial.append(linea.strip())
except FileNotFoundError:
    pass

ventana = tk.Tk()
ventana.title("App Clima")
ventana.geometry("650x600")
ventana.configure(bg="#34495E")
ventana.bind("<Return>", lambda event: obtener_clima())

titulo = tk.Label(
    ventana,
    text="🌦️ App del Clima",
    font=("Segoe UI", 16),
    bg="#34495E",
    fg="white"
)
titulo.pack(pady=15)

entrada = tk.Entry(
    ventana,
    font=("Segoe UI", 12),
    width=30,
    bd=0,
    justify="center"
)
entrada.pack(pady=10)

historial_label = tk.Label(
    ventana,
    width=40,
    height=15,
    bg="#34495E",
    fg="#ffffff",
    font=("Segoe UI", 12),
    bd=0,
    highlightthickness=0
)
historial_texto = "Historial (últimas búsquedas):\n" + "\n".join(historial[-5:])
historial_label.config(text=historial_texto)

def obtener_clima():
    ciudad = entrada.get()
    if not ciudad:
        resultado.config(text="Ingrese una ciudad")
        return
    resultado.config(text="🔎 Buscando...")
    ventana.update()
    url = f"https://wttr.in/{ciudad}?format=j1"
    try:
        respuesta = requests.get(url)
        datos = respuesta.json()
    except:
        resultado.config(text="Error de conexión")
        return
    ciudad_real = datos["nearest_area"][0]["areaName"][0]["value"]
    temperatura = datos["current_condition"][0]["temp_C"]
    clima = datos["current_condition"][0]["weatherDesc"][0]["value"]
    clima_lower = clima.lower()
    if "sun" in clima_lower:
        emoji = "☀️"
    elif "cloud" in clima_lower:
        emoji = "☁️"
    elif "rain" in clima_lower:
        emoji = "🌧️"
    else:
        emoji = "🌡️" 
    humedad = datos["current_condition"][0]["humidity"]
    texto = f"Ciudad: {ciudad_real}\nTemperatura: {temperatura}°C\nClima: {clima} {emoji}\nHumedad: {humedad}%"
    resultado.config(text=texto)
    entrada.delete(0, tk.END)
    if ciudad_real not in historial:
        historial.append(ciudad_real)
        with open("historial.txt", "a") as archivo:
            archivo.write(ciudad_real + "\n")

boton = tk.Button(
    ventana,
    text="Buscar",
    command=obtener_clima,
    bg="#4CAF50",
    fg="white",
    padx=10,      #padx = pixeles a la izquierda y la derecha del widget (en este caso del boton)
    pady=5,
    bd=0,
    font=("Segoe UI", 10)
)
boton.pack(pady=10)

resultado = tk.Label(
    ventana,
    text="",                  #text = texto en cuestion
    font=("Arial", 12),       #font = fuente de la letra
    justify="left",           #justify = alineacion del texto
    bg="#34495E",           #bg = color de fondo
    fg="white"                #fg = color de la letra
)
resultado.pack(pady=15)       #pady = agrega pixeles arriba y abajo del widget (en este caso del resultado)

historial_label.pack(pady=5, padx=5)

ventana.mainloop()