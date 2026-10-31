# Contenido editado — versión profesional
ESCENAS = [
('LoRA', 'Adaptación de bajo rango', [
 r'$W = W_0 + \frac{\alpha}{r}BA$',
 'Aprende una actualización pequeña sin reentrenar el modelo completo.',
 'Una clase visual: de la intuición al cálculo.'],
 'Pregunta inicial: ¿es realmente necesario modificar todos los pesos del modelo para aprender una tarea nueva? LoRA conserva el modelo base intacto y aprende únicamente una corrección de bajo rango. La ecuación de la portada será el mapa que guíe toda la clase.', 'portada'),
('El problema del ajuste completo', '01 · Motivación', [
 r'$h=W_0x,\qquad W_0\in\mathbb{R}^{d\times k}$',
 r'$W=W_0+\Delta W,\qquad N_{\mathrm{completo}}=dk$',
 'Cada parámetro entrenable exige gradientes y estados del optimizador.'],
 'x tiene k componentes y h tiene d. El ajuste completo modifica las d por k entradas de esta capa, además de requerir memoria para activaciones y estados del optimizador. El conteo corresponde a una matriz de pesos, sin incluir el sesgo.', ''),
('La idea central', '01 · Motivación', [
 'El modelo base permanece congelado durante todo el entrenamiento.',
 r'$\Delta W=sBA,\qquad s=\alpha/r$',
 'Solo A y B se optimizan en las capas seleccionadas.'],
 'LoRA significa Low-Rank Adaptation (adaptación de bajo rango). La restricción se aplica a la actualización aprendida, no al modelo base, que puede tener rango completo. s es un factor de escala. En esta clase también congelamos los sesgos.', 'ruta'),
('Las dimensiones encajan', '02 · Álgebra', [
 r'$x\in\mathbb{R}^{k},\quad A\in\mathbb{R}^{r\times k}$',
 r'$Ax\in\mathbb{R}^{r},\quad B\in\mathbb{R}^{d\times r}$',
 r'$B(Ax)\in\mathbb{R}^{d},\quad BA\in\mathbb{R}^{d\times k}$'],
 'La composición se lee de derecha a izquierda: A comprime la entrada de k coordenadas a r coordenadas, y B la expande de r a d. Así la corrección tiene exactamente las dimensiones de W0x y puede sumarse a ella. No hay activación no lineal entre A y B en LoRA básico.', 'dimensiones'),
('El recorrido de una entrada', '02 · Álgebra', [
 r'$h_0=W_0x$',
 r'$z=Ax,\qquad \delta h=sBz$',
 r'$h=h_0+\delta h$'],
 'La entrada sigue dos caminos en paralelo: el superior usa los pesos congelados del modelo base y el inferior calcula la corrección entrenable. Ambas salidas tienen d componentes y se suman coordenada a coordenada.', 'ruta'),
('Qué significa rango', '02 · Álgebra', [
 'El rango cuenta las direcciones linealmente independientes de una transformación.',
 r'$\mathrm{Im}(BA)\subseteq\mathrm{Im}(B)$',
 r'$\mathrm{rango}(BA)\leq\min(\mathrm{rango}(A),\mathrm{rango}(B))\leq r$'],
 'Cada salida BAx es una combinación de las columnas de B, por lo que vive en el espacio que ellas generan. Como hay r columnas, existen como máximo r direcciones independientes. La cota es a veces estricta: el rango real puede ser menor que r.', ''),
('Rango uno: una sola dirección', '02 · Geometría', [
 r'$r=1,\qquad B=b,\quad A=a^T$',
 r'$BAx=b(a^Tx)$',
 'La entrada determina el coeficiente; b fija la dirección.'],
 'El producto a transpuesta por x es un escalar, y multiplicar b por ese escalar produce puntos sobre una recta. La figura muestra las salidas de la corrección LoRA, no todas las salidas del modelo base.', 'rango'),
('Una suma de direcciones', '02 · Geometría', [
 r'$BA=\sum_{i=1}^{r}b_i a_i^T$',
 r'$BAx=\sum_{i=1}^{r}b_i(a_i^Tx)$',
 'Aumentar r da una actualización más expresiva.'],
 'b_i es la columna i de B y a_i transpuesta es la fila i de A. Cada producto exterior b_i a_i^T aporta una matriz de rango como máximo uno, de modo que la suma completa tiene rango como máximo r. Aumentar r eleva la capacidad y el costo, aunque no garantiza mejores resultados en validación.', ''),
('Cuántos parámetros entrenamos', '03 · Eficiencia', [
 r'$N_A=rk,\qquad N_B=dr$',
 r'$N_{\mathrm{LoRA}}=r(k+d)$',
 r'$\frac{N_{\mathrm{LoRA}}}{N_{\mathrm{completo}}}=\frac{r(k+d)}{dk}$'],
 'Contamos las entradas de A y B, no los grados de libertad independientes: la parametrización tiene redundancias y distintas parejas (A, B) pueden representar el mismo producto. El ahorro existe siempre que r(k+d) sea menor que dk.', ''),
('Ejemplo de ahorro', '03 · Eficiencia', [
 r'$d=k=4096,\qquad r=8$',
 r'$dk=16\,777\,216,\quad r(k+d)=65\,536$',
 r'$N_{\mathrm{LoRA}}/N_{\mathrm{completo}}=1/256\approx0.39\%$'],
 'Cifras calculadas para una sola matriz: entrenamos 256 veces menos parámetros en esa capa. Esto no implica 256 veces menos memoria total, pues el modelo base y las activaciones siguen ocupando memoria durante el entrenamiento.', 'barras'),
('El factor de escala', '03 · Hiperparámetros', [
 r'$s=\alpha/r,\qquad h=W_0x+sBAx$',
 r'$r=8,\ \alpha=16\quad\Longrightarrow\quad s=2$',
 'r controla la capacidad; α escala la magnitud de la corrección.'],
 'Usamos el escalado del artículo original. α no es el rango ni la tasa de aprendizaje: su efecto se combina con el optimizador y la inicialización, por lo que cambiarlo no equivale a cambiar solo la tasa de aprendizaje.', ''),
('Inicio sin alterar el modelo', '04 · Entrenamiento', [
 r'$A\sim\mathcal{N}(0,\sigma^2),\qquad B=0$',
 r'$BA=0\quad\Longrightarrow\quad h=W_0x$',
 'A rompe la simetría; B arranca con corrección nula.'],
 'El artículo inicializa A con una distribución gaussiana y B en cero: al comenzar, el comportamiento coincide exactamente con el modelo base. Si ambas matrices fueran cero, los gradientes del producto respecto de ambas también serían cero y no habría aprendizaje.', ''),
('La función que minimizamos', '04 · Entrenamiento', [
 r'$\mathcal{L}(A,B)=-\sum_{(x,y)\in\mathcal{D}}\sum_t\log p_{W_0+sBA}(y_t\mid x,y_{<t})$',
 'Cada término penaliza la baja probabilidad asignada al token correcto.',
 r'$(A^*,B^*)=\operatorname{argmin}_{A,B}\mathcal{L}(A,B)$'],
 'D es el conjunto de pares de entrada y respuesta; y_t es el token objetivo actual e y_{<t} son los tokens anteriores. Mostramos la suma de pérdidas, aunque en la práctica se suele promediar. La expresión W_0+sBA resume de forma abreviada la modificación de las matrices seleccionadas del modelo.', ''),
('Gradiente respecto de B', '04 · Regla de la cadena', [
 r'$z=Ax,\quad h=W_0x+sBz,\quad g=\nabla_h\mathcal{L}$',
 r'$\partial h_i/\partial B_{ij}=s z_j$',
 r'$\nabla_B\mathcal{L}=s\,g z^T\in\mathbb{R}^{d\times r}$'],
 'Derivación para un ejemplo y una sola aplicación de la capa. g mide cómo cambia la pérdida con cada componente de h, y al variar B_ij solo cambia h_i en s·z_j. Para un lote con varias posiciones de tokens se suman estas contribuciones.', ''),
('Gradiente respecto de A', '04 · Regla de la cadena', [
 r'$\nabla_z\mathcal{L}=sB^Tg$',
 r'$\partial z_i/\partial A_{ij}=x_j$',
 r'$\nabla_A\mathcal{L}=s(B^Tg)x^T\in\mathbb{R}^{r\times k}$'],
 'Primero trasladamos el gradiente hacia z mediante B transpuesta y después aplicamos z = Ax para obtener un producto exterior con x. Aunque W_0 no se actualiza, la retropropagación atraviesa el modelo para llegar a las capas anteriores.', ''),
('El primer paso de aprendizaje', '04 · Optimización', [
 r'$B=0\ \Longrightarrow\ \nabla_A\mathcal{L}=0$',
 r'$\nabla_B\mathcal{L}=s\,g(Ax)^T\quad\mathrm{puede\ ser\ no\ nulo}$',
 r'$B\leftarrow B-\eta\nabla_B\mathcal{L},\quad A\leftarrow A-\eta\nabla_A\mathcal{L}$'],
 'Esta actualización ilustra un paso de descenso de gradiente simple con tasa η, no la fórmula completa de Adam. Como B empieza en cero, A recibe gradiente nulo en el primer paso y B aprende primero; después ambos reciben gradientes no nulos. Ambos se calculan sobre el mismo estado, antes de actualizar ninguna matriz.', ''),
('Ejemplo numérico: los datos', '05 · Cálculo resuelto', [
 r'$d=k=2,\quad r=1,\quad \alpha=1,\quad s=1$',
 r'$W_0=I_2,\quad x=(1,2)^T$',
 r'$A=(1,-1),\qquad B=(2,1)^T$'],
 'Ejemplo didáctico con una pareja (A, B) que ya salió de la inicialización. W_0 es la matriz identidad. Aquí LoRA tiene cuatro parámetros, igual que la matriz completa de 2×2: elegimos dimensiones pequeñas para poder verificar cada cuenta a mano, no para demostrar ahorro.', 'matriz'),
('Ejemplo numérico: la salida', '05 · Cálculo resuelto', [
 r'$z=Ax=1\cdot1-1\cdot2=-1$',
 r'$BAx=(-2,-1)^T$',
 r'$h=(1,2)^T+(-2,-1)^T=(-1,1)^T$'],
 'A comprime las dos coordenadas de la entrada en el escalar −1 y B lo expande a la corrección (−2, −1). Al sumarla a la salida base (1, 2) obtenemos h = (−1, 1). Las flechas de la figura muestran esta suma vectorial.', 'vectores'),
('Ejemplo numérico: el gradiente', '05 · Cálculo resuelto', [
 r'$y=(0,0)^T,\quad\mathcal{L}=\frac{1}{2}\|h-y\|^2=1$',
 r'$g=h-y=(-1,1)^T,\quad\nabla_B\mathcal{L}=(1,-1)^T$',
 r'$B^Tg=-1,\quad\nabla_A\mathcal{L}=(-1,-2)$'],
 'Para poder verificar los gradientes a mano usamos una pérdida cuadrática, no la pérdida de lenguaje de la escena anterior. Como z = −1, g·z^T = (1, −1), y B^Tg = −1 multiplica a x^T para dar el gradiente de A.', ''),
('Una tasa demasiado grande', '05 · Cálculo resuelto', [
 r'$\eta=0.1:\quad A_{\mathrm{nuevo}}=(1.1,-0.8),\quad B_{\mathrm{nuevo}}=(1.9,1.1)^T$',
 r'$z_{\mathrm{nuevo}}=-0.5,\quad h_{\mathrm{nuevo}}=(0.05,1.45)^T$',
 r'$\mathcal{L}_{\mathrm{nueva}}=1.0525\ >\ 1$'],
 'Este paso, deliberadamente fallido, muestra que una tasa demasiado grande puede aumentar la pérdida incluso siguiendo el gradiente: no debemos prometer descenso para cualquier η. La siguiente escena reinicia desde el estado original, no desde este paso.', ''),
('Una tasa más pequeña', '05 · Cálculo resuelto', [
 r'$\eta=0.01:\quad A_{\mathrm{nuevo}}=(1.01,-0.98),\quad B_{\mathrm{nuevo}}=(1.99,1.01)^T$',
 r'$z_{\mathrm{nuevo}}=-0.95,\quad h_{\mathrm{nuevo}}=(-0.8905,1.0405)^T$',
 r'$\mathcal{L}_{\mathrm{nueva}}=0.93781525\ <\ 1$'],
 'Reiniciamos en A = (1, −1) y B = (2, 1). Con η = 0.01 la pérdida sí desciende. El contraste entre ambos pasos enseña una idea clave: LoRA sigue siendo un problema de optimización y exige elegir bien los hiperparámetros.', ''),
('LoRA dentro del Transformer', '06 · Aplicación', [
 r'$Q=XW_Q^T,\quad K=XW_K^T,\quad V=XW_V^T$',
 r'$W_Q=W_{Q0}+sB_QA_Q,\quad W_V=W_{V0}+sB_VA_V$',
 'Cada proyección seleccionada tiene su propia pareja (A, B).'],
 'Aquí X organiza los tokens por filas, por eso las matrices aparecen transpuestas. El artículo experimental con distintas proyecciones de atención, incluida la combinación query–value, aunque esa selección no es obligatoria: la configuración depende de la arquitectura y de la tarea.', ''),
('Fusión para inferencia', '06 · Uso del adaptador', [
 r'$W_{\mathrm{fusionado}}=W_0+sBA$',
 r'$h=W_{\mathrm{fusionado}}x$',
 'Guardar solo A y B permite reutilizar el mismo modelo base.'],
 'En la forma lineal básica podemos sumar la actualización a la matriz base y usar una única multiplicación por entrada: de ahí la ausencia de latencia extra en el método fusionado. El adaptador por sí solo no sustituye al modelo base; conservar una copia de este facilita cambiar de adaptador cuando se necesita.', 'fusion'),
('Resultados y límites', '07 · Lectura crítica', [
 'El artículo compara LoRA con ajuste completo en varios modelos.',
 'La calidad y el ahorro dependen de la tarea, el rango y las capas elegidas.',
 'El modelo base y las activaciones siguen ocupando memoria.'],
 'Los experimentos cubren RoBERTa, DeBERTa, GPT-2 y GPT-3, pero sus resultados no son garantía para cualquier tarea. LoRA no es cuantización por sí solo. Para elegir r, α y la tasa de aprendizaje, hay que usar un conjunto de validación separado del entrenamiento.', ''),
('La ecuación completa', '08 · Repaso', [
 r'$h=W_0x+\frac{\alpha}{r}B(Ax)$',
 r'$\mathrm{rango}(BA)\leq r,\qquad N=r(k+d)$',
 'LoRA aprende una corrección restringida con muy pocos parámetros.'],
 'Autoevaluación: ¿qué matriz no cambia durante el entrenamiento? ¿Por qué BA tiene rango como máximo r? ¿Por qué un adaptador requiere el modelo base? Cierre retomando la pregunta inicial de la clase.', ''),
('Fuente y práctica', '08 · Cierre', [
 'Hu et al. · LoRA: Low-Rank Adaptation of Large Language Models',
 'arXiv:2106.09685 · 2021 · secciones 2, 4, 5 y 7',
 'Práctica: recalcular el ejemplo con η = 0.005.'],
 'Fuente primaria: https://arxiv.org/abs/2106.09685. Enlace alternativo: https://huggingface.co/papers/2106.09685. Las derivaciones y el ejemplo en dos dimensiones son desarrollos didácticos propios de esta clase. Respuesta de la práctica: A = (1.005, −0.99), B = (1.995, 1.005), z = −0.975, h = (−0.945125, 1.020125).', '')
]

# Ampliación visual: artículo de IBM y documentación primaria contrastada.
NUEVAS = [
('Un modelo, varias tareas', '07 · Aplicaciones', [
 'Un mismo modelo base admite adaptadores distintos por tarea.',
 'Cada tarea aprende sus propias matrices A y B.',
 'El adaptador activo determina la corrección aplicada.'],
 'Ejemplos ilustrativos: resumir textos, seguir un formato de salida o responder con un estilo especializado. Cada tarea requiere datos adecuados y su propia evaluación, y cambiar de adaptador no garantiza que las respuestas sean correctas. Fuente complementaria: IBM, sección «Beneficios de LoRA».', 'tareas'),
('Una matriz de 4 × 4', '07 · Factorización visual', [
 r'$B\in\mathbb{R}^{4\times1},\quad A\in\mathbb{R}^{1\times4},\quad BA\in\mathbb{R}^{4\times4}$',
 'Ocho parámetros generan dieciséis entradas relacionadas.',
 r'$\mathrm{rango}(BA)\leq1$'],
 'Ejemplo propio con B = (1, 2, 3, 4)^T y A = (1, 0, −1, 2): cada fila del producto es un múltiplo de A, lo que hace visible por qué el resultado tiene rango uno aunque ocupe 4×4 entradas. La figura muestra la actualización BA, no una descomposición de W_0.', 'producto4'),
('El límite de la factorización', '07 · Precisión matemática', [
 r'$\mathrm{rango}(I_4)=4,\qquad\mathrm{rango}(BA)\leq1$',
 r'$I_4\neq BA\quad\mathrm{si}\quad B:4\times1,\ A:1\times4$',
 'LoRA restringe la actualización que aprende, no el modelo base.'],
 'El artículo divulgativo de IBM simplifica la factorización de una matriz 4×4. Una matriz arbitraria no admite representación exacta de rango uno: la identidad es un contraejemplo, pues sus columnas son linealmente independientes. Una aproximación de bajo rango puede tener error, pero LoRA básico aprende A y B directamente; no comienza comprimiendo todos los pesos del modelo.', 'identidad'),
('LoRA y QLoRA', '07 · Memoria', [
 'LoRA reduce la cantidad de parámetros entrenables.',
 'QLoRA almacena además el modelo base cuantizado a 4 bits.',
 'Los adaptadores se entrenan con cálculos de mayor precisión.'],
 'Fuente primaria: Dettmers et al., QLoRA, arXiv:2305.14314. La base cuantizada permanece congelada y los gradientes llegan solo a los adaptadores. Los 4 bits describen el almacenamiento de los pesos base, no todos los cálculos. El método combina NF4, doble cuantización y optimizadores paginados. El esquema es conceptual y no reporta cantidades exactas de VRAM.', 'qlora'),
('Configuración en PEFT', '07 · Python y Hugging Face', [
 'r: dimensión del espacio de actualización.',
 'lora_alpha: escala; target_modules: capas seleccionadas.',
 'lora_dropout: regularización en el camino del adaptador.'],
 'Ejemplo ilustrativo de LoraConfig: r=8, lora_alpha=16, target_modules=["q_proj","v_proj"], lora_dropout=0.05, bias="none". Los nombres de los módulos dependen de la arquitectura y hay que inspeccionar el modelo antes de configurarlos; no es una receta universal. Fuente: documentación oficial de Hugging Face PEFT, LoraConfig. Los valores mostrados son ejemplos, no resultados de un entrenamiento real.', 'config'),
('El flujo de entrenamiento', '07 · Proceso', [
 'Los datos definen la tarea y la señal de aprendizaje.',
 'La optimización actualiza A y B con el modelo base congelado.',
 'La validación guía los hiperparámetros y la selección final.'],
 'Separar entrenamiento, validación y prueba antes del ajuste evita evaluar sobre los mismos ejemplos usados para aprender. Calcular pérdida, retropropagar y actualizar los adaptadores constituye una iteración; la prueba se reserva para la evaluación final. Conviene guardar también la configuración y la identificación exacta del modelo base.', 'entrenar'),
('Capacidad y generalización', '07 · Límites', [
 'Un rango insuficiente puede limitar lo que el adaptador logra aprender.',
 'Un rango mayor añade parámetros y costo de entrenamiento.',
 'La validación comprueba si la mejora se generaliza a datos nuevos.'],
 'La restricción de rango y el sobreajuste son fenómenos distintos: sobreajustar significa que el desempeño aprendido no se generaliza, y no se deduce automáticamente de usar una factorización de bajo rango. Los diagramas esquematizan la capacidad de rango uno y dos, sin representar resultados experimentales.', 'capacidad')
]
ESCENAS[-2:-2] = NUEVAS