import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os


def tiempo_a_segundos(tiempo):
    partes = tiempo.split(":")

    if len(partes) == 3:
        horas, minutos, segundos = partes
        return int(horas) * 3600 + int(minutos) * 60 + float(segundos)

    elif len(partes) == 2:
        minutos, segundos = partes
        return int(minutos) * 60 + float(segundos)

    return float(tiempo)


def seleccionar_video():
    archivo = filedialog.askopenfilename(
        title="Seleccionar video",
        filetypes=[
            ("Videos", "*.mp4 *.mkv *.mov *.avi *.webm"),
            ("Todos los archivos", "*.*")
        ]
    )

    if archivo:
        video_var.set(archivo)


def crear_short():

    video = video_var.get()
    inicio = inicio_var.get()
    fin = fin_var.get()

    if not video:
        messagebox.showerror("Error", "Seleccioná un video.")
        return

    if not os.path.isfile(video):
        messagebox.showerror("Error", "El archivo no existe.")
        return

    try:
        inicio_segundos = tiempo_a_segundos(inicio)
        fin_segundos = tiempo_a_segundos(fin)

        duracion = fin_segundos - inicio_segundos

        if duracion <= 0:
            messagebox.showerror(
                "Error",
                "El tiempo de fin debe ser mayor que el inicio."
            )
            return

    except ValueError:
        messagebox.showerror(
            "Error",
            "Usá el formato HH:MM:SS"
        )
        return

    carpeta = os.path.join(
        os.path.dirname(video),
        "Shorts"
    )

    os.makedirs(carpeta, exist_ok=True)

    nombre = os.path.splitext(
        os.path.basename(video)
    )[0]

    salida = os.path.join(
        carpeta,
        nombre + "_short.mp4"
    )

    estado_var.set("🎬 Creando Short...")
    ventana.update()

    comando = [
        "ffmpeg",

        "-ss", str(inicio_segundos),
        "-i", video,

        "-t", str(duracion),

        "-vf",
        "scale=1080:1920:force_original_aspect_ratio=decrease,"
        "pad=1080:1920:(ow-iw)/2:(oh-ih)/2",

        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",

        "-c:a", "aac",
        "-b:a", "192k",

        "-movflags", "+faststart",

        "-y",
        salida
    ]

    resultado = subprocess.run(
        comando,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    if resultado.returncode == 0:

        estado_var.set("✅ Short creado correctamente")

        messagebox.showinfo(
            "Short creado",
            f"El Short fue creado correctamente.\n\n"
            f"{salida}"
        )

    else:

        estado_var.set("❌ Error al crear el Short")

        messagebox.showerror(
            "Error",
            "FFmpeg no pudo crear el Short."
        )


# -----------------------------
# VENTANA
# -----------------------------

ventana = tk.Tk()

ventana.title("Shorts Automatizados")

ventana.geometry("650x420")

ventana.resizable(False, False)


# Variables

video_var = tk.StringVar()
inicio_var = tk.StringVar(value="00:00:00")
fin_var = tk.StringVar(value="00:00:15")

estado_var = tk.StringVar(
    value="Esperando video..."
)


# Título

titulo = tk.Label(
    ventana,
    text="🎬 SHORTS AUTOMATIZADOS",
    font=("Arial", 20, "bold")
)

titulo.pack(pady=20)


# Video

tk.Label(
    ventana,
    text="Video:",
    font=("Arial", 11, "bold")
).pack(anchor="w", padx=40)

frame_video = tk.Frame(ventana)
frame_video.pack(fill="x", padx=40, pady=5)

entrada_video = tk.Entry(
    frame_video,
    textvariable=video_var,
    width=65
)

entrada_video.pack(
    side="left",
    fill="x",
    expand=True
)

tk.Button(
    frame_video,
    text="📁 Buscar",
    command=seleccionar_video
).pack(side="right", padx=5)


# Inicio

tk.Label(
    ventana,
    text="Inicio (HH:MM:SS):",
    font=("Arial", 11, "bold")
).pack(anchor="w", padx=40, pady=(15, 0))

tk.Entry(
    ventana,
    textvariable=inicio_var,
    width=20
).pack(anchor="w", padx=40)


# Fin

tk.Label(
    ventana,
    text="Fin (HH:MM:SS):",
    font=("Arial", 11, "bold")
).pack(anchor="w", padx=40, pady=(15, 0))

tk.Entry(
    ventana,
    textvariable=fin_var,
    width=20
).pack(anchor="w", padx=40)


# Botón

tk.Button(
    ventana,
    text="🎬 CREAR SHORT",
    command=crear_short,
    font=("Arial", 13, "bold"),
    padx=20,
    pady=10
).pack(pady=25)


# Estado

tk.Label(
    ventana,
    textvariable=estado_var,
    font=("Arial", 10)
).pack()


ventana.mainloop()
