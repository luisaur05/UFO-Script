# Proyecto de Animación de Nave en Blender con Interpolaciones

Este proyecto consiste en la creación y animación de una nave utilizando Blender y Python. El script automatiza la creación de objetos, la asignación de materiales, la configuración de cámaras, y la animación mediante interpolaciones de las trayectorias de la nave.

## Funcionalidades

### Purga de Objetos Huérfanos
La función `purge_orphans()` limpia objetos huérfanos en la escena para liberar memoria, adaptándose tanto a versiones de Blender anteriores a la 3.0 como a las versiones 3.0 y superiores.

### Limpieza de la Escena
`clean_scene()` elimina objetos existentes, colecciones, y materiales innecesarios en la escena para dejarla limpia y lista para nuevas adiciones.

### Configuración de la Cámara
La función `setup_camera()` agrega una cámara, la posiciona y la orienta según las coordenadas y rotaciones proporcionadas. Además, le asigna una propiedad para seguir a un objeto de control.

### Creación de Materiales
Las funciones `create_metal_ring_material()` y `create_floor_material()` crean materiales con diferentes propiedades como colores aleatorios y ajustes para reflejar o emitir luz. El material metálico se utiliza en el cuerpo de la nave y el material del piso en el plano donde la nave aterriza.

### Animación de la Nave
La función `animate_object()` asigna una trayectoria a la nave mediante interpolaciones entre los puntos clave. Utiliza las interpolaciones 'CUBIC' y 'BEZIER' para un movimiento más fluido.

### Creación de la Nave
`create_flying_saucer()` es la función principal que crea el modelo 3D de la nave. Incluye el cuerpo, la cúpula, las patas y luces de la nave. Además, aplica materiales como el material metálico para el cuerpo y materiales emisivos para las luces.

### Creación de la Ruta de la Nave
`create_path()` se encarga de crear una curva 3D, la cual representa el trayecto que seguirá la nave. Esta función acepta un conjunto de keyframes para definir las posiciones y tiempos de la nave.

## Estructura del Proyecto

### Funciones Clave:
- `purge_orphans()`: Elimina datos huérfanos en la escena.
- `clean_scene()`: Limpia la escena, eliminando objetos y colecciones no deseados.
- `add_ctrl_empty()`: Crea un objeto vacío de control en la escena.
- `track_empty()`: Agrega un control para que un objeto "mire" a un objetivo.
- `animate_object()`: Inserta keyframes para animar un objeto a lo largo de una trayectoria definida.
- `create_flying_saucer()`: Crea y monta la nave voladora con su geometría y materiales.
- `create_path()`: Genera una ruta para la animación de la nave.

### Objetos de la Nave:
1. **Cuerpo**: Una esfera uv achatada que representa el cuerpo de la nave.
2. **Cúpula**: Una esfera adicional agregada encima del cuerpo.
3. **Patas**: Cuatro patas cilíndricas agregadas en la parte inferior de la nave.
4. **Luces**: Ocho luces emisivas ubicadas en el cuerpo de la nave.

### Interpolaciones:
El movimiento de la nave se maneja mediante interpolaciones de tipo 'CUBIC' y 'BEZIER' para asegurar transiciones suaves entre los keyframes.

## Requisitos:
- Blender 3.x o superior.
- Conocimiento básico de scripting en Python para Blender.

## Cómo Ejecutar el Script:
1. Abre Blender.
2. Ve a la ventana de scripting.
3. Crea un nuevo script y copia el código.
4. Ejecútalo para crear y animar la nave voladora.

## Observaciones:
- Este proyecto utiliza materiales con nodos y configuraciones específicas para lograr efectos visuales realistas, como la emisión de luz en la nave.
- La animación de la nave se puede personalizar añadiendo o modificando los keyframes en la función `animate_object()`.





Demo video: https://youtu.be/ylmtM0hIKp8
