# Detector de Fraude Transaccional (Velocity Checks y Z-score)

Este es un script en Python nativo diseñado para procesar bases de datos transaccionales (archivos CSV) y detectar posibles fraudes utilizando análisis de velocidad. El algoritmo identifica usuarios que realizan múltiples transacciones en un periodo muy corto de tiempo y utiliza estadística básica para determinar si el comportamiento es anómalo.

##  Cómo funciona:

El proyecto no utiliza librerías externas. Todo el motor está construido con herramientas nativas de Python bajo el siguiente flujo:

1. *Ingesta de Datos:* Se utiliza csv.DictReader para leer de manera eficiente archivos CSV de gran volumen (probado con datasets de Kaggle).
2. *Transformación de Tiempo:* Las fechas en texto (%Y-%m-%d %H:%M:%S) se convierten a Segundos Absolutos (Unix Epoch) para permitir cálculos matemáticos entre transacciones.
3. *Algoritmo de Ventana Deslizante (Two-Pointer):* Se agrupan los historiales por ID (en este caso número de tarjeta) y se aplica una ventana de *5 minutos (300 segundos)*. Si un usuario tiene 3 o más transacciones en ese lapso temporal, se activa el filtro estadístico.
4. *Validación Estadística (Z-Score):* Se calcula la varianza y la desviación estándar poblacional del historial previo del usuario en tiempo real. 
   * *Bloqueo (Fraude):* Si el Z-Score de la transacción supera el umbral de 2 o -2.
   * *Revisión Manual:* Si el usuario no rebasa el umbral estadístico pero rompió la regla de velocidad, se le suma un punto de riesgo.

Nota técnica: El código incluye manejo de Edge Cases, al añadir el valor 0.0001 si la desviación estándar es 0 para evitar errores durante la ejecución.

## Tecnologías Utilizadas

* Python 3.x
* Librerías estándar: csv (lectura de datos), datetime (parseo temporal), math (operaciones de raíz cuadrada para la desviación estándar).

## Cómo ejecutar el proyecto

1. Clona este repositorio.
2. Descarga un dataset de transacciones (por ejemplo, el Credit Card Transactions Fraud Detection Dataset de Kaggle) y renómbralo a fraude_basedatos.csv.
3. Coloca el archivo .csv en la misma carpeta que el script.
4. Ejecuta el archivo desde tu terminal:
   ```bash
   python detector_main.py
*Nota: es importante que el csv que ocupes tenga algún tipo de ID (como número de tarjeta) que permita grupar las transacciones y una columna de tiempo con el formato %Y-%m-%d %H:%M:%S