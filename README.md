# 📊 Análisis de Ventas - Herramienta de Análisis

Este proyecto te permite analizar datos de ventas de manera completa y generar visualizaciones profesionales.

## 🚀 Características

- **Análisis estadístico completo** de datos de ventas
- **Visualizaciones automáticas** con gráficas profesionales
- **Análisis por categoría, región y tiempo**
- **Exportación de gráficas** en alta calidad
- **Interfaz fácil de usar** con reportes detallados

## 📋 Requisitos

Asegúrate de tener instaladas las siguientes librerías:

```bash
pip install -r requirements.txt
```

O instala manualmente:

```bash
pip install pandas matplotlib seaborn numpy openpyxl xlrd
```

## 📁 Estructura del Proyecto

```
analisis_ventas/
├── analisis_ventas.py      # Script principal de análisis
├── datos_ventas.csv        # Datos de ejemplo
├── requirements.txt        # Dependencias del proyecto
└── README.md              # Este archivo
```

## 🎯 Cómo Usar

### 1. Ejecutar el análisis completo

```bash
python analisis_ventas.py
```

### 2. Usar en tu propio código

```python
from analisis_ventas import AnalizadorVentas

# Crear analizador con tus datos
analizador = AnalizadorVentas('tu_archivo.csv')

# Generar reporte completo
analizador.generar_reporte_completo()

# O usar funciones específicas
analizador.mostrar_resumen_estadistico()
analizador.graficar_ventas_por_categoria()
```

## 📊 Formato de Datos

Tu archivo CSV debe tener las siguientes columnas:

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| fecha | Fecha de la venta | 2024-01-01 |
| producto | Nombre del producto | Laptop |
| categoria | Categoría del producto | Electrónicos |
| ventas | Monto de la venta | 1200.50 |
| cantidad | Cantidad vendida | 2 |
| region | Región de venta | Norte |

## 📈 Visualizaciones Generadas

El script genera las siguientes gráficas:

1. **Ventas por Categoría** - Gráfica de barras
2. **Distribución por Región** - Gráfica circular
3. **Evolución Temporal** - Gráfica de línea
4. **Productos Más Vendidos** - Gráfica horizontal

Todas las gráficas se guardan automáticamente como archivos PNG.

## 🔧 Personalización

Puedes personalizar el análisis modificando el archivo `analisis_ventas.py`:

- Cambiar colores de las gráficas
- Agregar nuevas métricas
- Modificar el formato de las visualizaciones
- Agregar nuevos tipos de análisis

## 📝 Ejemplo de Salida

```
🎯 ANÁLISIS DE VENTAS - HERRAMIENTA DE ANÁLISIS
==================================================
✅ Datos cargados exitosamente: 20 registros

==================================================
📊 RESUMEN ESTADÍSTICO DE VENTAS
==================================================
Total de ventas: $8,123.95
Promedio de ventas por transacción: $406.20
Venta máxima: $1,250.00
Venta mínima: $7.99
Total de productos vendidos: 52

📈 VENTAS POR CATEGORÍA:
  Electrónicos: $6,321.25
  Ropa: $1,256.22
  Educación: $546.48

🌍 VENTAS POR REGIÓN:
  Norte: $2,650.74
  Sur: $2,555.99
  Este: $1,464.24
  Oeste: $1,452.98
```

## 🤝 Contribuir

Si quieres mejorar este proyecto:

1. Haz un fork del repositorio
2. Crea una rama para tu feature
3. Haz commit de tus cambios
4. Abre un Pull Request

## 📞 Soporte

Si tienes problemas o preguntas:

- Revisa que todas las dependencias estén instaladas
- Verifica que tu archivo CSV tenga el formato correcto
- Asegúrate de que Python esté en tu PATH

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT. 