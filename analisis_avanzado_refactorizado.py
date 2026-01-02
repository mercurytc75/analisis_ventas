"""
Script para análisis avanzado de ventas.

Este script utiliza el paquete ventas_analytics para realizar análisis estadístico avanzado.
"""

import logging
from pathlib import Path

from ventas_analytics import (
    DataLoader,
    AnalizadorAvanzado,
    ConfiguracionVisualizacion
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Función principal para análisis avanzado."""
    print("🎯 ANÁLISIS AVANZADO DE VENTAS")
    print("=" * 50)
    
    try:
        # Cargar datos
        loader = DataLoader('datos_ventas.csv')
        datos = loader.cargar()
        
        # Crear analizador avanzado
        config = ConfiguracionVisualizacion()
        analizador = AnalizadorAvanzado(datos, config)
        
        print("\n" + "=" * 60)
        print("🚀 GENERANDO REPORTE AVANZADO DE ANÁLISIS")
        print("=" * 60)
        
        # Análisis de tendencias
        print("\n" + "=" * 50)
        print("📈 ANÁLISIS DE TENDENCIAS")
        print("=" * 50)
        tendencia = analizador.analizar_tendencias()
        print(f"Pendiente de la tendencia: {tendencia['pendiente']:.2f}")
        print(f"Coeficiente de correlación (R²): {tendencia['r_cuadrado']:.4f}")
        print(f"Valor p: {tendencia['valor_p']:.4f}")
        
        if tendencia['pendiente'] > 0:
            print("📈 Tendencia: CRECIENTE")
        elif tendencia['pendiente'] < 0:
            print("📉 Tendencia: DECRECIENTE")
        else:
            print("➡️ Tendencia: ESTABLE")
        
        analizador.graficar_tendencia()
        
        # Análisis de estacionalidad
        print("\n" + "=" * 50)
        print("📅 ANÁLISIS DE ESTACIONALIDAD")
        print("=" * 50)
        ventas_dia = analizador.obtener_ventas_por_dia_semana()
        print("Ventas por día de la semana:")
        for dia, venta in ventas_dia.items():
            print(f"  {dia}: ${venta:,.2f}")
        
        analizador.graficar_estacionalidad_semanal()
        
        # Análisis de correlaciones
        print("\n" + "=" * 50)
        print("🔗 ANÁLISIS DE CORRELACIONES")
        print("=" * 50)
        correlaciones = analizador.analizar_correlaciones()
        print("Matriz de correlaciones:")
        print(correlaciones)
        analizador.graficar_correlaciones()
        
        # Análisis de outliers
        print("\n" + "=" * 50)
        print("🔍 ANÁLISIS DE OUTLIERS")
        print("=" * 50)
        outliers, limites = analizador.detectar_outliers()
        print(f"Límite inferior: ${limites['limite_inferior']:.2f}")
        print(f"Límite superior: ${limites['limite_superior']:.2f}")
        print(f"Outliers detectados: {len(outliers)}")
        
        if len(outliers) > 0:
            print("\nOutliers encontrados:")
            for _, row in outliers.iterrows():
                print(f"  {row['fecha'].strftime('%Y-%m-%d')} - {row['producto']}: ${row['ventas']:.2f}")
        
        analizador.graficar_outliers()
        
        # Predicciones
        print("\n" + "=" * 50)
        print("🔮 PREDICCIÓN SIMPLE")
        print("=" * 50)
        predicciones = analizador.predecir_ventas(dias_futuros=5)
        print("Predicciones para los próximos 5 días:")
        for _, row in predicciones.iterrows():
            print(f"  {row['fecha'].strftime('%Y-%m-%d')}: ${row['prediccion']:.2f}")
        
        analizador.graficar_predicciones()
        
        print("\n✅ Reporte avanzado generado exitosamente!")
        print(f"📁 Todas las gráficas se han guardado en: {Path(config.directorio_salida).absolute()}")
        
    except FileNotFoundError as e:
        logger.error(f"Error: {e}")
        print(f"❌ Error: {e}")
    except ValueError as e:
        logger.error(f"Error de validación: {e}")
        print(f"❌ Error de validación: {e}")
    except Exception as e:
        logger.error(f"Error inesperado: {e}", exc_info=True)
        print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()

