# LoRA: guía del profesor

Duración sugerida de explicación: 35–45 minutos. Avance manual por pasos.

## 1. LoRA

Pregunta inicial: ¿es realmente necesario modificar todos los pesos del modelo para aprender una tarea nueva? LoRA conserva el modelo base intacto y aprende únicamente una corrección de bajo rango. La ecuación de la portada será el mapa que guíe toda la clase.

## 2. El problema del ajuste completo

x tiene k componentes y h tiene d. El ajuste completo modifica las d por k entradas de esta capa, además de requerir memoria para activaciones y estados del optimizador. El conteo corresponde a una matriz de pesos, sin incluir el sesgo.

## 3. La idea central

LoRA significa Low-Rank Adaptation (adaptación de bajo rango). La restricción se aplica a la actualización aprendida, no al modelo base, que puede tener rango completo. s es un factor de escala. En esta clase también congelamos los sesgos.

## 4. Las dimensiones encajan

La composición se lee de derecha a izquierda: A comprime la entrada de k coordenadas a r coordenadas, y B la expande de r a d. Así la corrección tiene exactamente las dimensiones de W0x y puede sumarse a ella. No hay activación no lineal entre A y B en LoRA básico.

## 5. El recorrido de una entrada

La entrada sigue dos caminos en paralelo: el superior usa los pesos congelados del modelo base y el inferior calcula la corrección entrenable. Ambas salidas tienen d componentes y se suman coordenada a coordenada.

## 6. Qué significa rango

Cada salida BAx es una combinación de las columnas de B, por lo que vive en el espacio que ellas generan. Como hay r columnas, existen como máximo r direcciones independientes. La cota es a veces estricta: el rango real puede ser menor que r.

## 7. Rango uno: una sola dirección

El producto a transpuesta por x es un escalar, y multiplicar b por ese escalar produce puntos sobre una recta. La figura muestra las salidas de la corrección LoRA, no todas las salidas del modelo base.

## 8. Una suma de direcciones

b_i es la columna i de B y a_i transpuesta es la fila i de A. Cada producto exterior b_i a_i^T aporta una matriz de rango como máximo uno, de modo que la suma completa tiene rango como máximo r. Aumentar r eleva la capacidad y el costo, aunque no garantiza mejores resultados en validación.

## 9. Cuántos parámetros entrenamos

Contamos las entradas de A y B, no los grados de libertad independientes: la parametrización tiene redundancias y distintas parejas (A, B) pueden representar el mismo producto. El ahorro existe siempre que r(k+d) sea menor que dk.

## 10. Ejemplo de ahorro

Cifras calculadas para una sola matriz: entrenamos 256 veces menos parámetros en esa capa. Esto no implica 256 veces menos memoria total, pues el modelo base y las activaciones siguen ocupando memoria durante el entrenamiento.

## 11. El factor de escala

Usamos el escalado del artículo original. α no es el rango ni la tasa de aprendizaje: su efecto se combina con el optimizador y la inicialización, por lo que cambiarlo no equivale a cambiar solo la tasa de aprendizaje.

## 12. Inicio sin alterar el modelo

El artículo inicializa A con una distribución gaussiana y B en cero: al comenzar, el comportamiento coincide exactamente con el modelo base. Si ambas matrices fueran cero, los gradientes del producto respecto de ambas también serían cero y no habría aprendizaje.

## 13. La función que minimizamos

D es el conjunto de pares de entrada y respuesta; y_t es el token objetivo actual e y_{<t} son los tokens anteriores. Mostramos la suma de pérdidas, aunque en la práctica se suele promediar. La expresión W_0+sBA resume de forma abreviada la modificación de las matrices seleccionadas del modelo.

## 14. Gradiente respecto de B

Derivación para un ejemplo y una sola aplicación de la capa. g mide cómo cambia la pérdida con cada componente de h, y al variar B_ij solo cambia h_i en s·z_j. Para un lote con varias posiciones de tokens se suman estas contribuciones.

## 15. Gradiente respecto de A

Primero trasladamos el gradiente hacia z mediante B transpuesta y después aplicamos z = Ax para obtener un producto exterior con x. Aunque W_0 no se actualiza, la retropropagación atraviesa el modelo para llegar a las capas anteriores.

## 16. El primer paso de aprendizaje

Esta actualización ilustra un paso de descenso de gradiente simple con tasa η, no la fórmula completa de Adam. Como B empieza en cero, A recibe gradiente nulo en el primer paso y B aprende primero; después ambos reciben gradientes no nulos. Ambos se calculan sobre el mismo estado, antes de actualizar ninguna matriz.

## 17. Ejemplo numérico: los datos

Ejemplo didáctico con una pareja (A, B) que ya salió de la inicialización. W_0 es la matriz identidad. Aquí LoRA tiene cuatro parámetros, igual que la matriz completa de 2×2: elegimos dimensiones pequeñas para poder verificar cada cuenta a mano, no para demostrar ahorro.

## 18. Ejemplo numérico: la salida

A comprime las dos coordenadas de la entrada en el escalar −1 y B lo expande a la corrección (−2, −1). Al sumarla a la salida base (1, 2) obtenemos h = (−1, 1). Las flechas de la figura muestran esta suma vectorial.

## 19. Ejemplo numérico: el gradiente

Para poder verificar los gradientes a mano usamos una pérdida cuadrática, no la pérdida de lenguaje de la escena anterior. Como z = −1, g·z^T = (1, −1), y B^Tg = −1 multiplica a x^T para dar el gradiente de A.

## 20. Una tasa demasiado grande

Este paso, deliberadamente fallido, muestra que una tasa demasiado grande puede aumentar la pérdida incluso siguiendo el gradiente: no debemos prometer descenso para cualquier η. La siguiente escena reinicia desde el estado original, no desde este paso.

## 21. Una tasa más pequeña

Reiniciamos en A = (1, −1) y B = (2, 1). Con η = 0.01 la pérdida sí desciende. El contraste entre ambos pasos enseña una idea clave: LoRA sigue siendo un problema de optimización y exige elegir bien los hiperparámetros.

## 22. LoRA dentro del Transformer

Aquí X organiza los tokens por filas, por eso las matrices aparecen transpuestas. El artículo experimental con distintas proyecciones de atención, incluida la combinación query–value, aunque esa selección no es obligatoria: la configuración depende de la arquitectura y de la tarea.

## 23. Fusión para inferencia

En la forma lineal básica podemos sumar la actualización a la matriz base y usar una única multiplicación por entrada: de ahí la ausencia de latencia extra en el método fusionado. El adaptador por sí solo no sustituye al modelo base; conservar una copia de este facilita cambiar de adaptador cuando se necesita.

## 24. Resultados y límites

Los experimentos cubren RoBERTa, DeBERTa, GPT-2 y GPT-3, pero sus resultados no son garantía para cualquier tarea. LoRA no es cuantización por sí solo. Para elegir r, α y la tasa de aprendizaje, hay que usar un conjunto de validación separado del entrenamiento.

## 25. Un modelo, varias tareas

Ejemplos ilustrativos: resumir textos, seguir un formato de salida o responder con un estilo especializado. Cada tarea requiere datos adecuados y su propia evaluación, y cambiar de adaptador no garantiza que las respuestas sean correctas. Fuente complementaria: IBM, sección «Beneficios de LoRA».

## 26. Una matriz de 4 × 4

Ejemplo propio con B = (1, 2, 3, 4)^T y A = (1, 0, −1, 2): cada fila del producto es un múltiplo de A, lo que hace visible por qué el resultado tiene rango uno aunque ocupe 4×4 entradas. La figura muestra la actualización BA, no una descomposición de W_0.

## 27. El límite de la factorización

El artículo divulgativo de IBM simplifica la factorización de una matriz 4×4. Una matriz arbitraria no admite representación exacta de rango uno: la identidad es un contraejemplo, pues sus columnas son linealmente independientes. Una aproximación de bajo rango puede tener error, pero LoRA básico aprende A y B directamente; no comienza comprimiendo todos los pesos del modelo.

## 28. LoRA y QLoRA

Fuente primaria: Dettmers et al., QLoRA, arXiv:2305.14314. La base cuantizada permanece congelada y los gradientes llegan solo a los adaptadores. Los 4 bits describen el almacenamiento de los pesos base, no todos los cálculos. El método combina NF4, doble cuantización y optimizadores paginados. El esquema es conceptual y no reporta cantidades exactas de VRAM.

## 29. Configuración en PEFT

Ejemplo ilustrativo de LoraConfig: r=8, lora_alpha=16, target_modules=["q_proj","v_proj"], lora_dropout=0.05, bias="none". Los nombres de los módulos dependen de la arquitectura y hay que inspeccionar el modelo antes de configurarlos; no es una receta universal. Fuente: documentación oficial de Hugging Face PEFT, LoraConfig. Los valores mostrados son ejemplos, no resultados de un entrenamiento real.

## 30. El flujo de entrenamiento

Separar entrenamiento, validación y prueba antes del ajuste evita evaluar sobre los mismos ejemplos usados para aprender. Calcular pérdida, retropropagar y actualizar los adaptadores constituye una iteración; la prueba se reserva para la evaluación final. Conviene guardar también la configuración y la identificación exacta del modelo base.

## 31. Capacidad y generalización

La restricción de rango y el sobreajuste son fenómenos distintos: sobreajustar significa que el desempeño aprendido no se generaliza, y no se deduce automáticamente de usar una factorización de bajo rango. Los diagramas esquematizan la capacidad de rango uno y dos, sin representar resultados experimentales.

## 32. La ecuación completa

Autoevaluación: ¿qué matriz no cambia durante el entrenamiento? ¿Por qué BA tiene rango como máximo r? ¿Por qué un adaptador requiere el modelo base? Cierre retomando la pregunta inicial de la clase.

## 33. Fuente y práctica

Fuente primaria: https://arxiv.org/abs/2106.09685. Enlace alternativo: https://huggingface.co/papers/2106.09685. Las derivaciones y el ejemplo en dos dimensiones son desarrollos didácticos propios de esta clase. Respuesta de la práctica: A = (1.005, −0.99), B = (1.995, 1.005), z = −0.975, h = (−0.945125, 1.020125).

Fuente: https://arxiv.org/abs/2106.09685
