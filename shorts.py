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

    else:
        return float(tiempo)


print("================================")
print("      SHORTS AUTOMATIZADOS")
print("================================")

video = input("Ruta del video: ").strip()
inicio = input("Tiempo de inicio (HH:MM:SS): ").strip()
fin = input("Tiempo de fin (HH:MM:SS): ").strip()

if not os.path.isfile(video):
    print("\n❌ No se encontró el video.")
    exit()

inicio_segundos = tiempo_a_segundos(inicio)
fin_segundos = tiempo_a_segundos(fin)

duracion = fin_segundos - inicio_segundos

if duracion <= 0:
    print("\n❌ El tiempo de fin debe ser mayor que el tiempo de inicio.")
    exit()

os.makedirs("Shorts", exist_ok=True)

nombre = os.path.splitext(os.path.basename(video))[0]
salida = f"Shorts/{nombre}_short.mp4"

print(f"\n⏱️ Duración del Short: {duracion:.2f} segundos")
print("🎬 Creando Short...")

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

resultado = subprocess.run(comando)

if resultado.returncode == 0:

    if os.path.exists(salida) and os.path.getsize(salida) > 0:
        print("\n================================")
        print("✅ SHORT CREADO CORRECTAMENTE")
        print("================================")
        print(f"📁 {os.path.abspath(salida)}")
        print(f"📦 Tamaño: {os.path.getsize(salida) / 1024 / 1024:.2f} MB")
    else:
        print("\n❌ FFmpeg terminó pero el archivo está vacío.")

else:
    print("\n❌ FFmpeg encontró un error.")
