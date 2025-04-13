import tkinter as tk
import json
import os
import random

# Función para cargar datos desde un archivo
def cargar_datos(archivo):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"preguntas": [], "f1": {}}

# Función para guardar datos en un archivo JSON
def guardar_datos(archivo, datos):
    try:
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
        print("Datos guardados correctamente.")
    except Exception as e:
        print(f"Error al guardar los datos: {e}")

class JuegoF1:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Adivina el Piloto de F1")
        self.ventana.geometry("600x400")
        self.ventana.resizable(False, False)

        self.datos = cargar_datos("f1_lista.json")
        # Seleccionar las primeras 10 preguntas (manteniendo el orden original)
        self.preguntas_random = self.datos["preguntas"][:10]
        self.pregunta_actual = 0
        self.respuestas = []
        self.pilotos_filtrados = self.datos["f1"].copy()  # Inicialmente, todos los pilotos están disponibles

        self.crear_primera_pantalla()

    def dibujar_bandera(self):
        # Se crea un frame contenedor para la bandera, para que se dibuje primero
        frame_fondo = tk.Frame(self.ventana)
        frame_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        for i in range(20):
            for j in range(20):
                color = "white" if (i + j) % 2 == 0 else "black"
                cuadro = tk.Frame(frame_fondo, bg=color, width=30, height=30)
                cuadro.place(x=j * 30, y=i * 30)

    def crear_primera_pantalla(self):
        # Dibujar la bandera a cuadros de fondo
        self.dibujar_bandera()

        # Elementos de la pantalla inicial
        self.titulo = tk.Label(self.ventana, text="¡Adivina el Piloto de F1!", font=("Arial", 16, "bold"), bg="black", fg="white")
        self.titulo.pack(pady=10)

        self.etiqueta_inicio = tk.Label(self.ventana, text="Presiona 'Empezar' para iniciar el juego.", font=("Arial", 12), wraplength=500, bg="black", fg="white")
        self.etiqueta_inicio.pack(pady=20)

        self.boton_empezar = tk.Button(self.ventana, text="Empezar", command=self.mostrar_segunda_pantalla, bg="#4CAF50", fg="white", width=15, height=2, font=("Arial", 14, "bold"))
        self.boton_empezar.pack(pady=10)

    def mostrar_segunda_pantalla(self):
        # Limpiar la primera pantalla
        for widget in self.ventana.winfo_children():
            widget.destroy()
        # Dibujar la bandera para la segunda pantalla
        self.dibujar_bandera()

        # Crear la pantalla de preguntas
        self.crear_interfaz_preguntas()

    def crear_interfaz_preguntas(self):
        # Elementos de la pantalla de preguntas sobre el fondo de bandera
        self.titulo = tk.Label(self.ventana, text="¡Responde las preguntas!", font=("Arial", 16, "bold"), bg="black", fg="white")
        self.titulo.pack(pady=10)

        self.contenedor_pregunta = tk.Frame(self.ventana, bg="black")
        self.contenedor_pregunta.pack(pady=20)

        self.etiqueta_pregunta = tk.Label(self.contenedor_pregunta, text="", font=("Arial", 12), wraplength=500, bg="black", fg="white")
        self.etiqueta_pregunta.pack()

        self.boton_si = tk.Button(self.ventana, text="Sí", command=lambda: self.responder(1), bg="#4CAF50", fg="white", width=10, height=2, font=("Arial", 14, "bold"))
        self.boton_no = tk.Button(self.ventana, text="No", command=lambda: self.responder(0), bg="#F44336", fg="white", width=10, height=2, font=("Arial", 14, "bold"))
        self.boton_si.pack(side=tk.LEFT, padx=20, pady=10)
        self.boton_no.pack(side=tk.RIGHT, padx=20, pady=10)

        self.etiqueta_resultado = tk.Label(self.ventana, text="", font=("Arial", 13), fg="red", bg="black")
        self.etiqueta_resultado.pack(pady=10)

        self.mostrar_pregunta()

    def mostrar_pregunta(self):
        # Mostrar la siguiente pregunta
        if self.pregunta_actual < len(self.preguntas_random):
            self.etiqueta_pregunta.config(text=self.preguntas_random[self.pregunta_actual])
        else:
            self.finalizar_juego()

    def responder(self, respuesta):
        # Guardar la respuesta del usuario
        self.respuestas.append(respuesta)

        # Filtrar los pilotos según las respuestas dadas hasta ahora
        self.pilotos_filtrados = {
            piloto: respuestas for piloto, respuestas in self.pilotos_filtrados.items()
            if respuestas[:len(self.respuestas)] == self.respuestas
        }

        # Continuar con las preguntas hasta llegar a la décima
        self.pregunta_actual += 1
        self.mostrar_pregunta()

    def finalizar_juego(self):
        # Intentar identificar el piloto después de 10 preguntas
        self.boton_si.config(state="disabled")
        self.boton_no.config(state="disabled")

        if len(self.pilotos_filtrados) == 1:
            mensaje = f"¡Tu piloto es: {list(self.pilotos_filtrados.keys())[0]}!"
        elif len(self.pilotos_filtrados) > 1:
            mensaje = f"No se pudo identificar con precisión. Los posibles pilotos son: {', '.join(self.pilotos_filtrados.keys())}."
        else:
            mensaje = "No se encontró coincidencia. Puedes agregar un nuevo piloto."
            self.pedir_nuevo_piloto()
        self.etiqueta_resultado.config(text=mensaje)

    def pedir_nuevo_piloto(self):
        self.etiqueta_pregunta.config(text="¿Cuál era el piloto?")
        self.entrada_piloto = tk.Entry(self.ventana)
        self.entrada_piloto.pack(pady=5)

        self.boton_guardar = tk.Button(self.ventana, text="Guardar", command=self.guardar_piloto, bg="#4CAF50", fg="white")
        self.boton_guardar.pack(pady=5)

    def guardar_piloto(self):
        nuevo_piloto = self.entrada_piloto.get().strip()
        if nuevo_piloto:
            self.datos["f1"][nuevo_piloto] = self.respuestas
            guardar_datos("f1_lista.json", self.datos)
            self.etiqueta_resultado.config(text=f"Piloto guardado: {nuevo_piloto}")
        self.entrada_piloto.destroy()
        self.boton_guardar.destroy()

# Función principal
def main():
    ventana = tk.Tk()
    app = JuegoF1(ventana)
    ventana.mainloop()

if __name__ == "__main__":
    main()
