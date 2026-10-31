# LoRA: clase visual con Python y FFmpeg

33 escenas y 99 pasos visuales. Estilo inspirado en la imagen y el fragmento de video aportados: fondo azul oscuro, títulos amarillos, tipografía matemática, ecuaciones progresivas y gráficos geométricos. Sin narración ni música. La presentación es un programa Python, no un archivo PowerPoint.

## Windows

1. Descomprime la carpeta completa.
2. Instala Python 3 (3.11 o posterior recomendado).
3. Ejecuta `instalar.bat` una vez.
4. Abre `presentar.bat`.
5. Pulsa F para pantalla completa. Espacio, flecha derecha o clic avanzan un paso. Flecha izquierda retrocede. Inicio y Fin van al primer y último paso. Esc cierra.

Las imágenes ya están generadas. Puedes presentar sin instalar FFmpeg. El texto explicativo para tu voz está en `Guion_del_profesor.md`. Para grabar tu clase, captura la ventana de presentación con tu grabador habitual.

## FFmpeg

Instala FFmpeg y comprueba en una terminal nueva que `ffmpeg -version` funciona. Después ejecuta `exportar_video.bat`. Genera `LoRA_completa.mp4` en 1920×1080 a 30 fps, sin audio, con cinco segundos por paso (8 min 15 s). Este tiempo es para el pase automático, no la duración recomendada de tu explicación.

Para cambiar el ritmo:

```bash
python clase.py video --segundos 12
```

El modo manual usa fundidos entre pasos. El MP4 usa apariciones por pasos a ritmo fijo. `Vista_previa.mp4` es una muestra de cuatro escenas, no la clase completa.

## Ubuntu

Necesitas Python 3, venv y Tk. Si falta Tk, el paquete del sistema es `python3-tk`.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python clase.py presentar
python clase.py video --segundos 5
```

## Editar

`escenas.py` contiene títulos, ecuaciones, notas y tipo de gráfico. `clase.py` define colores, posiciones, controles y exportación. Después de cambiar contenido ejecuta `python clase.py generar`. No necesitas LaTeX externo: las fórmulas usan MathText. Los PNG se renderizan a 1600×900; la exportación los escala a 1080p.

## Alcance matemático

Se explica LoRA original, con escala alfa/r y pesos base congelados. El ejemplo numérico y los gradientes son desarrollos didácticos propios. La pérdida cuadrática del ejemplo permite verificar las cuentas y no representa la pérdida de un modelo de lenguaje. La comparación de parámetros de 4096×4096 es un cálculo por matriz, no un benchmark.

Fuente: Hu et al., *LoRA: Low-Rank Adaptation of Large Language Models*, arXiv:2106.09685, secciones 2, 4, 5 y 7.
https://arxiv.org/abs/2106.09685
https://huggingface.co/papers/2106.09685

El diseño toma el estilo de las referencias; no incorpora sus logotipos, controles de YouTube ni fragmentos de video ajenos.


## Ampliación con el artículo de IBM

Se añaden siete escenas ilustradas: adaptadores por tarea, producto de matrices 4×1 y 1×4, limitaciones de rango, LoRA frente a QLoRA, configuración PEFT, entrenamiento y generalización. Los diagramas son originales y se generan con Python. La referencia de IBM se contrasta con el artículo original, el artículo de QLoRA y la documentación oficial de PEFT.

## Tu logo

Tu logo original está incluido como `logo.jpg` y aparece en la esquina superior derecha de las 33 escenas, conservando sus proporciones. La muestra de video también lo incluye. Para cambiarlo, reemplaza `logo.jpg` y ejecuta `regenerar.bat`. También se admite `logo.png`, que tiene prioridad si ambos archivos existen.

## Fuentes complementarias

- IBM: https://www.ibm.com/mx-es/think/topics/lora
- Hugging Face PEFT: https://huggingface.co/docs/peft/main/en/package_reference/lora
- Dettmers et al., QLoRA: https://arxiv.org/abs/2305.14314

Matices: LoRA entrena adaptadores; no elimina todo el entrenamiento. No toda matriz 4×4 puede factorizarse exactamente con rango uno. La restricción de rango no equivale al sobreajuste. Los cuatro bits de QLoRA describen almacenamiento de la base, no todos los cálculos.
