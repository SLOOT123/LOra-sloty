# Clase visual sobre LoRA

Presentación interactiva hecha con Python: 33 escenas y 99 pasos visuales sobre LoRA, QLoRA y PEFT. Incluye las imágenes ya generadas, una muestra de video y el [guion del profesor](Guion_del_profesor.md).

## Inicio rápido en Windows

1. Instala Python 3.11 o posterior.
2. Descarga el repositorio y descomprime la carpeta.
3. Ejecuta `instalar.bat` una vez para crear el entorno e instalar las dependencias.
4. Ejecuta `presentar.bat`.

No necesitas FFmpeg para presentar: las imágenes están incluidas en `pasos`.

### Controles

- **F**: pantalla completa.
- **Espacio**, **flecha derecha** o clic: avanzar.
- **Flecha izquierda**: retroceder.
- **Inicio** / **Fin**: ir al primer / último paso.
- **Esc**: cerrar.

## Crear un video

Para exportar la clase completa necesitas instalar [FFmpeg](https://ffmpeg.org/) y comprobar que `ffmpeg -version` funciona desde una terminal. Después, ejecuta `exportar_video.bat`. El video se genera como `LoRA_completa.mp4`, en 1920 × 1080 y sin audio.

También puedes elegir la duración de cada paso:

```bash
python clase.py video --segundos 12
```

`Vista_previa.mp4` es una muestra de cuatro escenas, no la clase completa.

## Ubuntu

Instala Python 3, `venv` y Tk (el paquete `python3-tk`, si hace falta). Desde la carpeta del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python clase.py presentar
```

Para exportar un video, instala FFmpeg y ejecuta:

```bash
python clase.py video --segundos 5
```

## Editar la presentación

- `escenas.py`: títulos, ecuaciones, notas y gráficos.
- `clase.py`: presentación, controles y exportación.
- `pasos/`: imágenes incluidas para presentar sin regenerarlas.

Después de editar el contenido, ejecuta `python clase.py generar`. Para más detalles sobre la generación, el logo y el alcance matemático, consulta [LEEME.md](LEEME.md).

## Referencias

- Hu et al., [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685).
- Dettmers et al., [QLoRA](https://arxiv.org/abs/2305.14314).
- [Documentación de LoRA en Hugging Face PEFT](https://huggingface.co/docs/peft/main/en/package_reference/lora).
