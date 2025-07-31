# 📋 INSTRUCCIONES DE USO - ANÁLISIS DE VENTAS

## 🚀 Inicio Rápido

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar análisis básico
```bash
python analisis_ventas.py
```

### 3. Ejecutar análisis avanzado
```bash
python analisis_avanzado.py
```

### 4. Usar dashboard interactivo
```bash
python dashboard_ventas.py
```

## 📁 Archivos del Proyecto

### Scripts Principales

| Archivo | Descripción | Uso |
|---------|-------------|-----|
| `analisis_ventas.py` | Análisis básico con visualizaciones | Análisis rápido y completo |
| `analisis_avanzado.py` | Análisis estadístico avanzado | Tendencias, correlaciones, predicciones |
| `dashboard_ventas.py` | Dashboard interactivo | Análisis personalizado paso a paso |

### Datos y Configuración

| Archivo | Descripción |
|---------|-------------|
| `datos_ventas.csv` | Datos de ejemplo |
| `requirements.txt` | Dependencias del proyecto |
| `README.md` | Documentación completa |

## 🎯 Cómo Usar Cada Script

### 1. Análisis Básico (`analisis_ventas.py`)

**¿Cuándo usarlo?** Para un análisis rápido y completo de tus datos.

**Qué hace:**
- ✅ Carga y valida los datos
- 📊 Genera estadísticas básicas
- 📈 Crea 4 visualizaciones automáticas
- 💾 Guarda gráficas como PNG

**Ejecución:**
```bash
python analisis_ventas.py
```

**Salida esperada:**
```
🎯 ANÁLISIS DE VENTAS - HERRAMIENTA DE ANÁLISIS
==================================================
✅ Datos cargados exitosamente: 20 registros

📊 RESUMEN ESTADÍSTICO DE VENTAS
Total de ventas: $7,729.44
Promedio de ventas por transacción: $386.47
...
```

### 2. Análisis Avanzado (`analisis_avanzado.py`)

**¿Cuándo usarlo?** Para análisis estadístico profundo y predicciones.

**Qué hace:**
- 📈 Análisis de tendencias con regresión lineal
- 📅 Análisis de estacionalidad semanal
- 🔗 Matriz de correlaciones
- 🔍 Detección de outliers
- 🔮 Predicciones para próximos 5 días

**Ejecución:**
```bash
python analisis_avanzado.py
```

**Salida esperada:**
```
🎯 ANÁLISIS AVANZADO DE VENTAS
==================================================
📈 ANÁLISIS DE TENDENCIAS
Pendiente: -8.72
R²: 0.1234
📉 Tendencia: DECRECIENTE
...
```

### 3. Dashboard Interactivo (`dashboard_ventas.py`)

**¿Cuándo usarlo?** Para análisis personalizado y exploración interactiva.

**Qué hace:**
- 🎯 Menú interactivo con 9 opciones
- 📊 Análisis a la carta
- 🎨 Visualizaciones personalizadas
- 💾 Exportación a Excel
- 🔄 Navegación fácil

**Ejecución:**
```bash
python dashboard_ventas.py
```

**Opciones del menú:**
```
🎯 DASHBOARD DE ANÁLISIS DE VENTAS
============================================================
1. 📊 Resumen estadístico básico
2. 📈 Análisis de tendencias
3. 📅 Análisis de estacionalidad
4. 🔗 Análisis de correlaciones
5. 🔍 Detección de outliers
6. 🔮 Predicciones
7. 📋 Reporte completo
8. 🎨 Visualizaciones personalizadas
9. 💾 Exportar datos procesados
0. 🚪 Salir
```

## 📊 Formato de Datos Requerido

Tu archivo CSV debe tener estas columnas:

```csv
fecha,producto,categoria,ventas,cantidad,region
2024-01-01,Laptop,Electrónicos,1200.50,2,Norte
2024-01-02,Smartphone,Electrónicos,800.00,1,Sur
...
```

### Especificaciones:
- **fecha**: Formato YYYY-MM-DD
- **producto**: Nombre del producto
- **categoria**: Categoría del producto
- **ventas**: Monto en dólares (decimal)
- **cantidad**: Número entero
- **region**: Región de venta

## 📈 Visualizaciones Generadas

### Análisis Básico
1. `ventas_por_categoria.png` - Gráfica de barras
2. `ventas_por_region.png` - Gráfica circular
3. `evolucion_ventas.png` - Gráfica de línea temporal
4. `productos_mas_vendidos.png` - Gráfica horizontal

### Análisis Avanzado
1. `tendencia_ventas.png` - Análisis de tendencia
2. `estacionalidad_semanal.png` - Patrones semanales
3. `correlaciones.png` - Matriz de correlaciones
4. `outliers_ventas.png` - Detección de outliers
5. `prediccion_ventas.png` - Predicciones futuras

## 🔧 Personalización

### Cambiar colores de gráficas
Edita el archivo `analisis_ventas.py`:
```python
# Línea 58: Cambiar color de barras
bars = plt.bar(ventas_categoria.index, ventas_categoria.values, color='tu_color')
```

### Agregar nuevas métricas
En `analisis_avanzado.py`, agrega nuevas funciones:
```python
def nueva_metrica(self):
    # Tu código aquí
    pass
```

### Modificar formato de fechas
En cualquier script:
```python
# Para formato diferente
self.datos['fecha'] = pd.to_datetime(self.datos['fecha'], format='%d/%m/%Y')
```

## 🚨 Solución de Problemas

### Error: "No module named 'pandas'"
```bash
pip install pandas matplotlib seaborn numpy scipy openpyxl xlrd
```

### Error: "File not found"
- Verifica que `datos_ventas.csv` esté en el mismo directorio
- O especifica la ruta completa en el script

### Error: "Invalid date format"
- Asegúrate de que las fechas estén en formato YYYY-MM-DD
- O modifica el formato en el código

### Gráficas no se muestran
- En Windows, puede que necesites un backend de matplotlib
- Agrega esta línea al inicio del script:
```python
import matplotlib
matplotlib.use('TkAgg')
```

## 📞 Soporte

### Verificar instalación
```bash
python -c "import pandas, matplotlib, seaborn, scipy; print('✅ Todas las librerías instaladas')"
```

### Verificar datos
```bash
python -c "import pandas; df = pandas.read_csv('datos_ventas.csv'); print(df.head())"
```

### Logs de error
Si hay errores, revisa:
1. Que todas las dependencias estén instaladas
2. Que el archivo CSV tenga el formato correcto
3. Que Python esté en tu PATH

## 🎯 Próximos Pasos

1. **Personaliza los datos**: Reemplaza `datos_ventas.csv` con tus propios datos
2. **Ajusta las visualizaciones**: Modifica colores, tamaños y estilos
3. **Agrega nuevas métricas**: Implementa análisis específicos para tu negocio
4. **Automatiza reportes**: Configura ejecución automática con cron o Task Scheduler

¡Disfruta analizando tus ventas! 🚀 