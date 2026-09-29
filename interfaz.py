import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import vlc

from shorts import crear_short


class ShortsApp:

    def __init__(self, ventana):
        self.ventana = ventana

        self.ventana.title("UA Devs Shorts V0.4")
        self.ventana.geometry("900x760")
        self.ventana.resizable(False, False)

        self.video = None
        self.duracion = 0

        self.inicio = 0
        self.fin = 15
        self.posicion = 0

        self.reproduciendo = False

        # VLC
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        self.crear_interfaz()

        # Actualizar posición del video
        self.actualizar_posicion()

    # =====================================================
    # INTERFAZ
    # =====================================================

    def crear_interfaz(self):

        titulo = tk.Label(
            self.ventana,
            text="🎬 UA Devs Shorts",
            font=("Arial", 24, "bold")
        )

        titulo.pack(pady=10)

        subtitulo = tk.Label(
            self.ventana,
            text="Editor de Shorts V0.4",
            font=("Arial", 10)
        )

        subtitulo.pack()

        # =================================================
        # SELECCIONAR VIDEO
        # =================================================

        tk.Button(
            self.ventana,
            text="📁 Seleccionar video",
            font=("Arial", 12, "bold"),
            command=self.seleccionar_video
        ).pack(pady=8)

        self.nombre_video = tk.Label(
            self.ventana,
            text="Ningún video seleccionado",
            font=("Arial", 10)
        )

        self.nombre_video.pack()

        # =================================================
        # VIDEO
        # =================================================

        self.video_frame = tk.Frame(
            self.ventana,
            bg="black",
            width=800,
            height=400
        )

        self.video_frame.pack(pady=12)

        self.video_frame.pack_propagate(False)

        # =================================================
        # TIEMPO ACTUAL
        # =================================================

        self.tiempo_actual = tk.StringVar(
            value="00:00 / 00:00"
        )

        tk.Label(
            self.ventana,
            textvariable=self.tiempo_actual,
            font=("Arial", 12, "bold")
        ).pack()

        # =================================================
        # BARRA DE PROGRESO
        # =================================================

        self.progreso = tk.Scale(
            self.ventana,
            from_=0,
            to=100,
            orient="horizontal",
            length=750,
            showvalue=False,
            command=self.mover_video
        )

        self.progreso.pack()

        # =================================================
        # CONTROLES
        # =================================================

        controles = tk.Frame(self.ventana)

        controles.pack(pady=5)

        tk.Button(
            controles,
            text="⏪ -5s",
            width=8,
            command=lambda: self.saltar(-5)
        ).grid(row=0, column=0, padx=3)

        tk.Button(
            controles,
            text="▶ Reproducir",
            width=12,
            command=self.reproducir
        ).grid(row=0, column=1, padx=3)

        tk.Button(
            controles,
            text="⏸ Pausar",
            width=10,
            command=self.pausar
        ).grid(row=0, column=2, padx=3)

        tk.Button(
            controles,
            text="⏹ Detener",
            width=10,
            command=self.detener
        ).grid(row=0, column=3, padx=3)

        tk.Button(
            controles,
            text="+5s ⏩",
            width=8,
            command=lambda: self.saltar(5)
        ).grid(row=0, column=4, padx=3)

        # =================================================
        # MARCAR INICIO / FIN
        # =================================================

        marcadores = tk.Frame(self.ventana)

        marcadores.pack(pady=10)

        tk.Button(
            marcadores,
            text="🟢 Marcar inicio",
            font=("Arial", 11, "bold"),
            command=self.marcar_inicio
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            marcadores,
            text="🔴 Marcar fin",
            font=("Arial", 11, "bold"),
            command=self.marcar_fin
        ).grid(row=0, column=1, padx=10)

        # =================================================
        # INFORMACIÓN
        # =================================================

        informacion = tk.Frame(self.ventana)

        informacion.pack(pady=5)

        tk.Label(
            informacion,
            text="Inicio:"
        ).grid(row=0, column=0, padx=5)

        self.inicio_var = tk.StringVar(
            value="00:00"
        )

        tk.Label(
            informacion,
            textvariable=self.inicio_var,
            font=("Arial", 11, "bold")
        ).grid(row=0, column=1, padx=5)

        tk.Label(
            informacion,
            text="Fin:"
        ).grid(row=0, column=2, padx=5)

        self.fin_var = tk.StringVar(
            value="00:15"
        )

        tk.Label(
            informacion,
            textvariable=self.fin_var,
            font=("Arial", 11, "bold")
        ).grid(row=0, column=3, padx=5)

        tk.Label(
            informacion,
            text="Duración:"
        ).grid(row=0, column=4, padx=5)

        self.duracion_short_var = tk.StringVar(
            value="15 segundos"
        )

        tk.Label(
            informacion,
            textvariable=self.duracion_short_var,
            font=("Arial", 11, "bold")
        ).grid(row=0, column=5, padx=5)

        # =================================================
        # SLIDER INICIO
        # =================================================

        tk.Label(
            self.ventana,
            text="🟢 Punto de inicio"
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

        # =================================================
        # SLIDER FIN
        # =================================================

        tk.Label(
            self.ventana,
            text="🔴 Punto final"
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

        # =================================================
        # CREAR SHORT
        # =================================================

        tk.Button(
            self.ventana,
            text="🎬 CREAR SHORT",
            font=("Arial", 14, "bold"),
            padx=25,
            pady=8,
            command=self.generar_short
        ).pack(pady=10)

        # =================================================
        # ESTADO
        # =================================================

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
            pady=5
        )

    # =====================================================
    # SELECCIONAR VIDEO
    # =====================================================

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

        self.obtener_duracion()

        media = self.instance.media_new(archivo)

        self.player.set_media(media)

        self.player.set_xwindow(
            self.video_frame.winfo_id()
        )

        self.estado.config(
            text="✅ Video cargado"
        )

    # =====================================================
    # DURACIÓN
    # =====================================================

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
                "No se pudo obtener la duración."
            )

            return

        self.progreso.config(
            to=self.duracion
        )

        self.slider_inicio.config(
            to=self.duracion
        )

        self.slider_fin.config(
            to=self.duracion
        )

        self.inicio = 0
        self.fin = min(15, self.duracion)

        self.slider_inicio.set(self.inicio)
        self.slider_fin.set(self.fin)

        self.actualizar_informacion()

    # =====================================================
    # REPRODUCCIÓN
    # =====================================================

    def reproducir(self):

        if not self.video:

            messagebox.showwarning(
                "Video",
                "Primero seleccioná un video."
            )

            return

        self.player.play()

        self.reproduciendo = True

        self.estado.config(
            text="▶ Reproduciendo..."
        )

    def pausar(self):

        self.player.pause()

        self.reproduciendo = False

        self.estado.config(
            text="⏸ Pausado"
        )

    def detener(self):

        self.player.stop()

        self.reproduciendo = False

        self.estado.config(
            text="⏹ Detenido"
        )

    # =====================================================
    # SALTAR
    # =====================================================

    def saltar(self, segundos):

        if not self.video:
            return

        posicion = self.player.get_time()

        nueva_posicion = posicion + segundos * 1000

        nueva_posicion = max(
            0,
            min(
                nueva_posicion,
                int(self.duracion * 1000)
            )
        )

        self.player.set_time(
            int(nueva_posicion)
        )

    # =====================================================
    # MOVER VIDEO
    # =====================================================

    def mover_video(self, valor):

        if not self.video:
            return

        posicion = float(valor)

        self.player.set_time(
            int(posicion * 1000)
        )

    # =====================================================
    # ACTUALIZAR POSICIÓN
    # =====================================================

    def actualizar_posicion(self):

        if self.video:

            posicion = self.player.get_time()

            if posicion >= 0:

                segundos = posicion / 1000

                self.posicion = segundos

                self.progreso.set(
                    segundos
                )

                self.tiempo_actual.set(
                    f"{self.formatear_tiempo(segundos)} / "
                    f"{self.formatear_tiempo(self.duracion)}"
                )

        self.ventana.after(
            200,
            self.actualizar_posicion
        )

    # =====================================================
    # MARCAR INICIO
    # =====================================================

    def marcar_inicio(self):

        if not self.video:
            return

        self.inicio = self.posicion

        if self.inicio >= self.fin:

            self.fin = min(
                self.duracion,
                self.inicio + 1
            )

            self.slider_fin.set(
                self.fin
            )

        self.slider_inicio.set(
            self.inicio
        )

        self.actualizar_informacion()

    # =====================================================
    # MARCAR FIN
    # =====================================================

    def marcar_fin(self):

        if not self.video:
            return

        self.fin = self.posicion

        if self.fin <= self.inicio:

            self.inicio = max(
                0,
                self.fin - 1
            )

            self.slider_inicio.set(
                self.inicio
            )

        self.slider_fin.set(
            self.fin
        )

        self.actualizar_informacion()

    # =====================================================
    # SLIDER INICIO
    # =====================================================

    def cambiar_inicio(self, valor):

        self.inicio = float(valor)

        if self.inicio >= self.fin:

            self.inicio = max(
                0,
                self.fin - 1
            )

            self.slider_inicio.set(
                self.inicio
            )

        self.actualizar_informacion()

    # =====================================================
    # SLIDER FIN
    # =====================================================

    def cambiar_fin(self, valor):

        self.fin = float(valor)

        if self.fin <= self.inicio:

            self.fin = min(
                self.duracion,
                self.inicio + 1
            )

            self.slider_fin.set(
                self.fin
            )

        self.actualizar_informacion()

    # =====================================================
    # INFORMACIÓN
    # =====================================================

    def actualizar_informacion(self):

        self.inicio_var.set(
            self.formatear_tiempo(self.inicio)
        )

        self.fin_var.set(
            self.formatear_tiempo(self.fin)
        )

        duracion = self.fin - self.inicio

        self.duracion_short_var.set(
            f"{duracion:.1f} segundos"
        )

    # =====================================================
    # FORMATEAR TIEMPO
    # =====================================================

    def formatear_tiempo(self, segundos):

        minutos = int(segundos // 60)

        segundos_restantes = int(
            segundos % 60
        )

        return (
            f"{minutos:02d}:"
            f"{segundos_restantes:02d}"
        )

    # =====================================================
    # CREAR SHORT
    # =====================================================

    def generar_short(self):

        if not self.video:

            messagebox.showwarning(
                "Video",
                "Primero seleccioná un video."
            )

            return

        duracion = self.fin - self.inicio

        if duracion <= 0:

            messagebox.showerror(
                "Error",
                "El intervalo seleccionado no es válido."
            )

            return

        if duracion > 60:

            messagebox.showerror(
                "Error",
                "El Short no puede superar los 60 segundos."
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
                f"Short creado correctamente.\n\n"
                f"Duración: {duracion:.1f} segundos\n\n"
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


# =========================================================
# INICIAR
# =========================================================

ventana = tk.Tk()

app = ShortsApp(ventana)

ventana.mainloop()