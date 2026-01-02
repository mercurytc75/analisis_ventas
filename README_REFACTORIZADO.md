# 📊 Análisis de Ventas - Herramienta de Análisis Profesional

Este proyecto proporciona una solución profesional y escalable para analizar datos de ventas, generar estadísticas y crear visualizaciones de alta calidad.

## 🚀 Características

- **Arquitectura modular** y escalable
- **Análisis estadístico completo** de datos de ventas
- **Análisis avanzado** (tendencias, correlaciones, predicciones, outliers)
- **Visualizaciones automáticas** con gráficas profesionales
- **Análisis por categoría, región y tiempo**
- **Exportación de gráficas** en alta calidad (PNG)
- **Exportación de datos** a Excel y CSV
- **Dashboard interactivo** para análisis personalizado
- **Código limpio** siguiendo principios SOLID
- **Type hints** y documentación completa
- **Manejo robusto de errores** y logging

## 📋 Requisitos

Asegúrate de tener instaladas las siguientes librerías:

```bash
pip install -r requirements.txt
```

O instala manualmente:

```bash
pip install pandas matplotlib seaborn numpy scipy openpyxl xlrd
```

## 📁 Estructura del Proyecto

```
analisis_ventas/
├── ventas_analytics/          # Paquete principal (código modular)
│   ├── __init__.py           # Inicialización del paquete
│   ├── config.py             # Configuración centralizada
│   ├── data.py               # Carga y validación de datos
│   ├── statistics.py         # Cálculo de estadísticas
│   ├── visualization.py      # Generación de visualizaciones
│   ├── reporting.py          # Presentación de reportes
│   ├── advanced.py           # Análisis avanzado
│   └── export.py             # Exportación de datos
│
├── analisis_basico.py        # Script para análisis básico
├── analisis_avanzado_refactorizado.py  # Script para análisis avanzado
├── dashboard_refactorizado.py # Dashboard interactivo
│
├── datos_ventas.csv          # Datos de ejemplo
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Este archivo
```

## 🎯 Cómo Usar

### Opción 1: Análisis Básico

Ejecuta el script de análisis básico:

```bash
python analisis_basico.py
```

Este script genera:
- Resumen estadístico completo
- 4 visualizaciones (categorías, regiones, evolución temporal, productos)

### Opción 2: Análisis Avanzado

Ejecuta el script de análisis avanzado:

```bash
python analisis_avanzado_refactorizado.py
```

Este script incluye:
- Análisis de tendencias con regresión lineal
- Análisis de estacionalidad semanal
- Matriz de correlaciones
- Detección de outliers
- Predicciones de ventas

### Opción 3: Dashboard Interactivo

Ejecuta el dashboard interactivo:

```bash
python dashboard_refactorizado.py
```

El dashboard te permite:
- Navegar por diferentes análisis
- Generar reportes completos
- Exportar datos procesados
- Ver visualizaciones personalizadas

### Opción 4: Usar como Biblioteca

Puedes importar el paquete en tu propio código:

```python
from ventas_analytics import (
    DataLoader,
    EstadisticasVentas,
    VisualizadorVentas,
    AnalizadorAvanzado,
    ExportadorDatos,
    ConfiguracionVisualizacion
)

# Cargar datos
loader = DataLoader('datos_ventas.csv')
datos = loader.cargar()

# Calcular estadísticas
estadisticas = EstadisticasVentas(datos)
resumen = estadisticas.obtener_resumen_general()

# Crear visualizaciones
config = ConfiguracionVisualizacion(directorio_salida='graficas/')
visualizador = VisualizadorVentas(config)
ventas_cat = estadisticas.obtener_ventas_por_categoria()
visualizador.graficar_barras(
    datos=ventas_cat,
    titulo='Ventas por Categoría',
    etiqueta_x='Categoría',
    etiqueta_y='Ventas ($)',
    nombre_archivo='ventas_categoria.png'
)

# Análisis avanzado
analizador_av = AnalizadorAvanzado(datos, config)
tendencia = analizador_av.analizar_tendencias()
predicciones = analizador_av.predecir_ventas(dias_futuros=7)

# Exportar datos
exportador = ExportadorDatos(estadisticas)
exportador.exportar_excel('reporte.xlsx')
```

## 📊 Formato de Datos

Tu archivo CSV debe tener las siguientes columnas:

| Columna | Descripción | Ejemplo | Tipo |
|---------|-------------|---------|------|
| fecha | Fecha de la venta | 2024-01-01 | Fecha |
| producto | Nombre del producto | Laptop | Texto |
| categoria | Categoría del producto | Electrónicos | Texto |
| ventas | Monto de la venta | 1200.50 | Numérico |
| cantidad | Cantidad vendida | 2 | Numérico |
| region | Región de venta | Norte | Texto |

## 🏗️ Arquitectura

El proyecto sigue principios de código limpio y arquitectura modular:

### Módulos Principales

1. **`config.py`**: Configuración centralizada (colores, estilos, tamaños)
2. **`data.py`**: Carga y validación de datos con manejo de errores robusto
3. **`statistics.py`**: Cálculo de estadísticas básicas y agrupaciones
4. **`visualization.py`**: Generación de visualizaciones (barras, líneas, tortas, etc.)
5. **`reporting.py`**: Formateo y presentación de reportes
6. **`advanced.py`**: Análisis avanzado (tendencias, correlaciones, predicciones)
7. **`export.py`**: Exportación de datos a diferentes formatos

### Principios de Diseño

- **SOLID**: Cada clase tiene una responsabilidad única
- **DRY**: Sin duplicación de código
- **Type Hints**: Tipado estático para mejor mantenibilidad
- **Logging**: Sistema de logging profesional
- **Validación**: Validación exhaustiva de datos
- **Extensibilidad**: Fácil agregar nuevas funcionalidades

## 📈 Visualizaciones Generadas

El sistema puede generar las siguientes visualizaciones:

1. **Gráficas de Barras** - Ventas por categoría, productos más vendidos
2. **Gráficas de Torta** - Distribución por región
3. **Gráficas de Línea** - Evolución temporal, tendencias, predicciones
4. **Boxplots** - Detección de outliers
5. **Heatmaps** - Matriz de correlaciones

Todas las gráficas se guardan automáticamente como archivos PNG de alta calidad.

## 🔧 Personalización

Puedes personalizar el análisis modificando la configuración:

```python
from ventas_analytics import ConfiguracionVisualizacion

# Crear configuración personalizada
config = ConfiguracionVisualizacion(
    figsize_standard=(12, 8),
    dpi=300,
    paleta_colores=['#FF0000', '#00FF00', '#0000FF'],
    directorio_salida='mis_graficas/',
    estilo_plt='seaborn-v0_8'
)
```

## 📝 Ejemplos de Uso

### Ejemplo 1: Análisis Rápido

```python
from ventas_analytics import DataLoader, EstadisticasVentas, PresentadorReporte

loader = DataLoader('datos_ventas.csv')
datos = loader.cargar()
estadisticas = EstadisticasVentas(datos)
PresentadorReporte.mostrar_resumen_estadistico(estadisticas)
```

### Ejemplo 2: Análisis con Visualizaciones

```python
from ventas_analytics import (
    DataLoader, EstadisticasVentas, VisualizadorVentas
)

loader = DataLoader('datos_ventas.csv')
datos = loader.cargar()
estadisticas = EstadisticasVentas(datos)
visualizador = VisualizadorVentas()

# Gráfica de categorías
ventas_cat = estadisticas.obtener_ventas_por_categoria()
visualizador.graficar_barras(
    datos=ventas_cat,
    titulo='Ventas por Categoría',
    etiqueta_x='Categoría',
    etiqueta_y='Ventas ($)',
    nombre_archivo='categorias.png'
)
```

### Ejemplo 3: Análisis Avanzado

```python
from ventas_analytics import DataLoader, AnalizadorAvanzado

loader = DataLoader('datos_ventas.csv')
datos = loader.cargar()
analizador = AnalizadorAvanzado(datos)

# Analizar tendencias
tendencia = analizador.analizar_tendencias()
print(f"Tendencia: {tendencia['pendiente']:.2f}")
print(f"R²: {tendencia['r_cuadrado']:.4f}")

# Predecir ventas
predicciones = analizador.predecir_ventas(dias_futuros=7)
print(predicciones)

# Detectar outliers
outliers, limites = analizador.detectar_outliers()
print(f"Outliers encontrados: {len(outliers)}")
```

## 🧪 Testing

El código está diseñado para ser fácil de testear. Cada módulo puede probarse de forma independiente:

```python
# Ejemplo de test para DataLoader
def test_cargar_datos():
    loader = DataLoader('datos_ventas.csv')
    datos = loader.cargar()
    assert not datos.empty
    assert 'ventas' in datos.columns
```

## 🤝 Contribuir

Si quieres mejorar este proyecto:

1. Haz un fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Haz commit de tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📞 Soporte

Si tienes problemas o preguntas:

- Revisa que todas las dependencias estén instaladas
- Verifica que tu archivo CSV tenga el formato correcto
- Asegúrate de que Python 3.8+ esté instalado
- Revisa los logs para más información de errores

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🎓 Recursos Adicionales

- Documentación de pandas: https://pandas.pydata.org/docs/
- Documentación de matplotlib: https://matplotlib.org/stable/contents.html
- Documentación de seaborn: https://seaborn.pydata.org/

