# Propuesta de diseño

##  Justificación del proyecto y revisión bibliográfica

## Descripción y síntesis del problema

El problema radica en la necesidad de realizar analisis de manera objetiva y cuantificable de las emociones que se generan en los espectadores durante una pelicula en una sala de cine. Debido a que los métodos tradicionales como las encuestas presentan limitaciones significativas como lo puede ser el sesgo, falta de correlación temporal entre las emociones y el estímulo, y la incapacidad de capturar reacciones espontaneas y no verbalizadas.

Entonces en este proyecto se busca capturar, analizar y clasificar de forma no intrusiva las emociones, en tiempo real y con alta precisión, las expresiones faciales de los espectadores en la sala de cine durante la función. Ademas que el sistema funcione en una red de nodos que permita recolectar los datos a un servidor central.


## Gestión de los requerimientos
### Esquema de Codificación de Requerimientos

- Prefijo RF: Requerimiento Funcional
- Prefijo RNF: Requerimiento No Funcional

Sufijo Categoría:

- CAP: Captura de imágenes
- PRO: Procesamiento
- CLA: Clasificación
- ALM: Almacenamiento
- COM: Comunicación
- SEG: Seguridad
- REN: Rendimiento
- USE: Usabilidad
## Tabla de requerimientos principales para el proyecto

| ID | Categoría | Descripción | Criterio de Aceptación | Prioridad |
|---|----------|------------|----------------------|---------|
| RF-CAP-01 | Captura | Sistema captura imágenes faciales en baja luz | Captura en ≤ 5 lux | Alta |
| RF-CAP-02 | Captura | Captura no intrusiva, camuflada en asientos | Sin interferencia visible | Alta |
| RF-PRO-01 | Procesamiento | Detección de rostros en imágenes | Precisión ≥ 90% | Alta |
| RF-CLA-01 | Clasificación | Clasificar 6 emociones básicas | Enojo, disgusto, miedo, felicidad, tristeza, sorpresa | Alta |
| RF-CLA-02 | Clasificación | Procesamiento local (Edge AI) | Sin envío externo de imágenes | Alta |
| RF-ALM-01 | Almacenamiento | Registro con marca temporal | Precisión ≤ 100ms | Alta |
| RF-COM-01 | Comunicación | Acceso remoto para configuración y además permitir transferencia de metadatos para su posterior análisis | Conexion remota por medio de SSH y capacidad para conectarse a una base de datos | Media |
| RNF-HW-01 | Hardware | Implementación en Raspberry Pi | RPi con mín. 4GB RAM | Alta |
| RNF-REN-01 | Rendimiento | Baja latencia de procesamiento | ≤ 300ms captura-clasificación | Alta |
| RNF-SEG-01 | Seguridad | No almacenar imágenes originales | Solo metadatos | Alta |
| RNF-USE-01 | Usabilidad | Operación autónoma | ≥ 8 horas sin intervención | Alta |
| RNF-DEP-01 | Dependencias | Yocto Project y TensorFlow Lite | Imagen Linux personalizada | Alta |

# Requerimientos especificos

| ID | Descripción | Criterio de Aceptación | Prioridad |
|---|------------|----------------------|---------|
| RNF-HW-01 | Utilizar Raspberry Pi como unidad central de procesamiento | Capacidad suficiente para realizar la inferencia con poca latencia > 300ms | Alta |
| RNF-HW-02 | Cámara con sensibilidad infrarroja para captura en baja luz | Tener sensibilidad a la luz infrarroja | Alta |
| RNF-HW-03 | Iluminador IR discreto para mejorar captura en oscuridad | LED IR 850nm con difusor, invisible al ojo humano | Media |
| RNF-HW-04 | Sistema de alimentación PoE (Power over Ethernet) | Estándar IEEE 802.3at (PoE+) con protección sobrecarga | Alta |
| RNF-HW-05 | Disipación térmica pasiva (sin ventiladores) | Temperatura máxima en operación ≤ 65°C | Alta |
| RNF-HW-06 | Carcasa integrable en respaldar de asiento de cine | Dimensiones máximas: 10cm × 8cm × 3cm | Alta |
| RNF-HW-07 | Material de carcasa no reflectante | Acabado mate con coeficiente reflexión < 10% | Media |
| RNF-HW-08 | Almacenamiento local para sistema operativo y datos | SSD M.2 o microSD Clase 10 UHS-I con mín. 32GB | Alta |
| RNF-HW-10 | Posicionamiento ajustable de cámara | Rango ajuste vertical: ±20°, horizontal: ±15° | Media |
| RNF-HW-11 | Consumo energético en operación continua | Máximo 15W promedio, pico 25W | Alta |
| RNF-HW-13 | Indicadores LED de estado operativo | 3 LEDs mínimo: encendido, procesamiento, error | Baja |
| RNF-HW-14 | Botón físico para reinicio seguro | Accesible pero protegido contra activación accidental | Media |
| RNF-HW-18 | Sistema de montaje seguro y removible | Soportar 5kg de fuerza sin desprenderse | Alta |



## Vista operacional del sistema

## Vista funcional del sistema

## Arquitectura del sistema propuesto

### Diagrama del sistema:

![image](./fig/Arquitectura_del_sistema_propuesto.png)

## Análisis de dependencias

### Meta-layers necesarias a nivel de yocto:
- meta-poky: Capa base de Yocto Project con funcionalidad esencial
- meta-raspberrypi: Agrega soporte para la Raspberry Pi 5
- meta-openembedded/meta-oe: Proporciona componentes adicionales para sistemas embebidos
- meta-openembedded/meta-networking: Agrega soporte para las conexiones a internet
- meta-openembedded/meta-python: Agrega soporte básico para Python
- meta-openembedded/meta-multimedia: Proporciona soporte para cámaras y procesamiento multimedia
- meta-tensorflow-lite: Agrega soporte para TensorFlow Lite y sus dependencias
- meta-opencv: Proporciona soporte para OpenCV y bibliotecas de visión por computador
- meta-facial-detection (capa personalizada): Capa propia para la aplicación de análisis facial

### Árbol de dependencias:
```
meta-facial-detection
├── meta-opencv
│   └── meta-openembedded/meta-multimedia
├── meta-tensorflow-lite
│   ├── meta-openembedded/meta-python
│   └── meta-openembedded/meta-oe
├── meta-raspberrypi
│   └── meta-poky
├── meta-openembedded/meta-networking
└── meta-poky
```

## Estrategia de integración de la solución

## Planeamiento de la ejecución

## Conclusiones
