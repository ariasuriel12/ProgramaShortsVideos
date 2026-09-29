import subprocess
import os


def crear_short(video, inicio, fin, salida=None):
    duracion = fin - inicio

    if duracion <= 0:
        raise ValueError("El tiempo de fin debe ser mayor que el inicio.")

    if not os.path.isfile(video):
        raise FileNotFoundError("El video no existe.")

    if salida is None:
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

    comando = [
        "ffmpeg",
        "-ss", str(inicio),
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

    resultado = subprocess.run(comando)

    if resultado.returncode != 0:
        raise RuntimeError("FFmpeg no pudo crear el Short.")

    return salida
