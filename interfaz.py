import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import vlc

from shorts import crear_short


class ShortsApp:

    def __init__(self, ventana):
        self.ventana = ventana

        self.ventana.title("UA Devs Shorts")
        self.ventana.geometry("900x700")
        self.ventana.resizable(False, False)

        self.video = None
        self.duracion = 0

        self.inicio = 0
        self.fin = 15

        # VLC
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        self.crear_interfaz()

    # -----------------------------------------
    # INTERFAZ
    # -----------------------------------------

    def crear_interfaz(self):

        titulo = tk.Label(
            self.ventana,
            text="🎬 UA Devs Shorts",
            font=("Arial", 24, "bold")
        )

        titulo.pack(pady=15)

        # Seleccionar video
        tk.Button(
            self.ventana,
            text="📁 Seleccionar video",
            font=("Arial", 12, "bold"),
            command=self.seleccionar_video
        ).pack(pady=5)

        self.nombre_video = tk.Label(
            self.ventana,
            text="Ningún video seleccionado",
            font=("Arial", 10)
        )

        self.nombre_video.pack(pady=5)

        # -----------------------------------------
        # VIDEO
        # -----------------------------------------

        self.video_frame = tk.Frame(
            self.ventana,
            bg="black",
            width=800,
            height=430
        )

        self.video_frame.pack(pady=15)

        self.video_frame.pack_propagate(False)

        # -----------------------------------------
        # CONTROLES
        # -----------------------------------------

        controles = tk.Frame(self.ventana)

        controles.pack(pady=5)

        tk.Button(
            controles,
            text="▶ Reproducir",
            command=self.reproducir
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            controles,
            text="⏸ Pausar",
            command=self.pausar
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            controles,
            text="⏹ Detener",
            command=self.detener
        ).grid(row=0, column=2, padx=5)

        # -----------------------------------------
        # TIEMPOS
        # -----------------------------------------

        tiempos = tk.Frame(self.ventana)

        tiempos.pack(pady=10)

        tk.Label(
            tiempos,
            text="Inicio:"
        ).grid(row=0, column=0, padx=10)

        self.inicio_var = tk.StringVar(value="00:00")

        tk.Label(
            tiempos,
            textvariable=self.inicio_var,
            font=("Arial", 12, "bold")
        ).grid(row=0, column=1, padx=10)

        tk.Label(
            tiempos,
            text="Fin:"
        ).grid(row=0, column=2, padx=10)

        self.fin_var = tk.StringVar(value="00:15")

        tk.Label(
            tiempos,
            textvariable=self.fin_var,
            font=("Arial", 12, "bold")
        ).grid(row=0, column=3, padx=10)

        # -----------------------------------------
        # SLIDER INICIO
        # -----------------------------------------

        tk.Label(
            self.ventana,
            text="🟢 Inicio del Short"
        ).pack()

        self.slider_inicio = tk.Scale(
            self.ventana,
            from_=0,
            to=100,
            orient="horizontal",
            length=750,
            command=self.cambiar_inicio
        )

        self.slider_inicio.pack()

        # -----------------------------------------
        # SLIDER FIN
        # -----------------------------------------

        tk.Label(
            self.ventana,
            text="🔴 Fin del Short"
        ).pack()

        self.slider_fin = tk.Scale(
            self.ventana,
            from_=0,
            to=100,
            orient="horizontal",
            length=750,
            command=self.cambiar_fin
        )

        self.slider_fin.pack()

        # -----------------------------------------
        # CREAR SHORT
        # -----------------------------------------

        tk.Button(
            self.ventana,
            text="🎬 CREAR SHORT",
            font=("Arial", 14, "bold"),
            padx=25,
            pady=10,
            command=self.generar_short
        ).pack(pady=15)

        # -----------------------------------------
        # ESTADO
        # -----------------------------------------

        self.estado = tk.Label(
            self.ventana,
            text="Esperando video...",
            font=("Arial", 10)
        )

        self.estado.pack()

        # Firma
        tk.Label(
            self.ventana,
            text="Desarrollado por UA Devs",
            font=("Arial", 9, "italic")
        ).pack(
            side="bottom",
            anchor="e",
            padx=15,
            pady=8
        )

    # -----------------------------------------
    # SELECCIONAR VIDEO
    # -----------------------------------------

    def seleccionar_video(self):

        archivo = filedialog.askopenfilename(
            title="Seleccionar video",
            filetypes=[
                (
                    "Videos",
                    "*.mp4 *.mkv *.mov *.avi *.webm"
                ),
                (
                    "Todos los archivos",
                    "*.*"
                )
            ]
        )

        if not archivo:
            return

        self.video = archivo

        self.nombre_video.config(
            text=os.path.basename(archivo)
        )

        # Obtener duración
        self.obtener_duracion()

        # Cargar video en VLC
        media = self.instance.media_new(archivo)

        self.player.set_media(media)

        # Conectar VLC con Tkinter
        self.player.set_xwindow(
            self.video_frame.winfo_id()
        )

        self.estado.config(
            text="✅ Video cargado"
        )

    # -----------------------------------------
    # OBTENER DURACIÓN
    # -----------------------------------------

    def obtener_duracion(self):

        comando = [
            "ffprobe",
            "-v", "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            self.video
        ]

        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True
        )

        try:
            self.duracion = float(
                resultado.stdout.strip()
            )

        except ValueError:
            messagebox.showerror(
                "Error",
                "No se pudo obtener la duración del video."
            )
            return

        self.slider_inicio.config(
            to=self.duracion
        )

        self.slider_fin.config(
            to=self.duracion
        )

        # Fin inicial = 15 segundos
        self.fin = min(15, self.duracion)

        self.slider_inicio.set(0)
        self.slider_fin.set(self.fin)

        self.actualizar_tiempos()

    # -----------------------------------------
    # CAMBIAR INICIO
    # -----------------------------------------

    def cambiar_inicio(self, valor):

        self.inicio = float(valor)

        if self.inicio >= self.fin:
            self.inicio = max(0, self.fin - 1)
            self.slider_inicio.set(self.inicio)

        self.actualizar_tiempos()

    # -----------------------------------------
    # CAMBIAR FIN
    # -----------------------------------------

    def cambiar_fin(self, valor):

        self.fin = float(valor)

        if self.fin <= self.inicio:
            self.fin = min(
                self.duracion,
                self.inicio + 1
            )

            self.slider_fin.set(self.fin)

        self.actualizar_tiempos()

    # -----------------------------------------
    # ACTUALIZAR TIEMPOS
    # -----------------------------------------

    def actualizar_tiempos(self):

        self.inicio_var.set(
            self.formatear_tiempo(self.inicio)
        )

        self.fin_var.set(
            self.formatear_tiempo(self.fin)
        )

    def formatear_tiempo(self, segundos):

        minutos = int(segundos // 60)
        segundos_restantes = int(segundos % 60)

        return f"{minutos:02d}:{segundos_restantes:02d}"

    # -----------------------------------------
    # REPRODUCIR
    # -----------------------------------------

    def reproducir(self):

        if not self.video:
            messagebox.showwarning(
                "Video",
                "Primero seleccioná un video."
            )
            return

        self.player.play()

        self.estado.config(
            text="▶ Reproduciendo..."
        )

    # -----------------------------------------
    # PAUSAR
    # -----------------------------------------

    def pausar(self):

        self.player.pause()

        self.estado.config(
            text="⏸ Video pausado"
        )

    # -----------------------------------------
    # DETENER
    # -----------------------------------------

    def detener(self):

        self.player.stop()

        self.estado.config(
            text="⏹ Video detenido"
        )

    # -----------------------------------------
    # CREAR SHORT
    # -----------------------------------------

    def generar_short(self):

        if not self.video:
            messagebox.showwarning(
                "Video",
                "Primero seleccioná un video."
            )
            return

        try:

            self.estado.config(
                text="🎬 Creando Short..."
            )

            self.ventana.update()

            salida = crear_short(
                self.video,
                self.inicio,
                self.fin
            )

            self.estado.config(
                text="✅ Short creado correctamente"
            )

            messagebox.showinfo(
                "Short creado",
                f"El Short fue creado correctamente.\n\n"
                f"{salida}"
            )

        except Exception as error:

            self.estado.config(
                text="❌ Error"
            )

            messagebox.showerror(
                "Error",
                str(error)
            )


# -----------------------------------------
# INICIAR APP
# -----------------------------------------

ventana = tk.Tk()

app = ShortsApp(ventana)

ventana.mainloop()
