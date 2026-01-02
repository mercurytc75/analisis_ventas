"""
Script principal para análisis básico de ventas.

Este script utiliza el paquete ventas_analytics para realizar un análisis completo.
"""

import logging
from pathlib import Path

from ventas_analytics import (
    DataLoader,
    EstadisticasVentas,
    VisualizadorVentas,
    PresentadorReporte,
    ConfiguracionVisualizacion
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AnalizadorVentas:
    """
    Clase principal para análisis de ventas.
    
    Esta clase orquesta todas las operaciones de análisis, estadísticas
    y visualizaciones siguiendo el principio de responsabilidad única.
    """
    
    def __init__(
        self,
        archivo_datos: str,
        config_visualizacion: ConfiguracionVisualizacion = None
    ):
        """
        Inicializar el analizador de ventas.
        
        Args:
            archivo_datos: Ruta al archivo CSV con datos de ventas.
            config_visualizacion: Configuración para visualizaciones. Si es None, usa valores por defecto.
        """
        self.loader = DataLoader(archivo_datos)
        self.config = config_visualizacion or ConfiguracionVisualizacion()
        self.visualizador = VisualizadorVentas(self.config)
        self._datos = None
        self._estadisticas = None
    
    def cargar_datos(self) -> None:
        """Cargar datos desde el archivo."""
        self._datos = self.loader.cargar()
        self._estadisticas = EstadisticasVentas(self._datos)
    
    @property
    def datos(self):
        """Obtener los datos cargados."""
        if self._datos is None:
            self.cargar_datos()
        return self._datos
    
    @property
    def estadisticas(self):
        """Obtener el calculador de estadísticas."""
        if self._estadisticas is None:
            self.cargar_datos()
        return self._estadisticas
    
    def mostrar_resumen_estadistico(self) -> None:
        """Mostrar resumen estadístico en consola."""
        PresentadorReporte.mostrar_resumen_estadistico(self.estadisticas)
    
    def graficar_ventas_por_categoria(self) -> None:
        """Crear gráfica de ventas por categoría."""
        datos = self.estadisticas.obtener_ventas_por_categoria()
        self.visualizador.graficar_barras(
            datos=datos,
            titulo='Ventas Totales por Categoría',
            etiqueta_x='Categoría',
            etiqueta_y='Ventas ($)',
            nombre_archivo='ventas_por_categoria.png'
        )
    
    def graficar_ventas_por_region(self) -> None:
        """Crear gráfica de ventas por región."""
        datos = self.estadisticas.obtener_ventas_por_region()
        self.visualizador.graficar_torta(
            datos=datos,
            titulo='Distribución de Ventas por Región',
            nombre_archivo='ventas_por_region.png'
        )
    
    def graficar_evolucion_ventas(self) -> None:
        """Crear gráfica de evolución de ventas en el tiempo."""
        datos = self.estadisticas.obtener_evolucion_temporal()
        self.visualizador.graficar_linea_temporal(
            datos=datos,
            columna_fecha='fecha',
            columna_valor='ventas',
            titulo='Evolución de Ventas Diarias',
            etiqueta_x='Fecha',
            etiqueta_y='Ventas ($)',
            nombre_archivo='evolucion_ventas.png'
        )
    
    def graficar_productos_mas_vendidos(self) -> None:
        """Crear gráfica de productos más vendidos."""
        datos = self.estadisticas.obtener_productos_mas_vendidos()
        self.visualizador.graficar_barras(
            datos=datos,
            titulo='Productos Más Vendidos (por cantidad)',
            etiqueta_x='Cantidad Vendida',
            etiqueta_y='Producto',
            nombre_archivo='productos_mas_vendidos.png',
            orientacion_horizontal=True
        )
    
    def generar_reporte_completo(self) -> None:
        """Generar un reporte completo con todas las visualizaciones."""
        logger.info("Iniciando generación de reporte completo")
        
        print("\n" + "=" * 60)
        print("🚀 GENERANDO REPORTE COMPLETO DE ANÁLISIS DE VENTAS")
        print("=" * 60)
        
        # Mostrar resumen estadístico
        self.mostrar_resumen_estadistico()
        
        # Generar todas las gráficas
        print("\n📊 Generando visualizaciones...")
        try:
            self.graficar_ventas_por_categoria()
            self.graficar_ventas_por_region()
            self.graficar_evolucion_ventas()
            self.graficar_productos_mas_vendidos()
            
            print("\n✅ Reporte completo generado exitosamente!")
            print(f"📁 Las gráficas se han guardado en: {Path(self.config.directorio_salida).absolute()}")
        except Exception as e:
            logger.error(f"Error al generar visualizaciones: {e}", exc_info=True)
            raise


def main() -> None:
    """Función principal del programa."""
    print("🎯 ANÁLISIS DE VENTAS - HERRAMIENTA DE ANÁLISIS")
    print("=" * 50)
    
    try:
        # Crear instancia del analizador
        analizador = AnalizadorVentas('datos_ventas.csv')
        
        # Generar reporte completo
        analizador.generar_reporte_completo()
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

