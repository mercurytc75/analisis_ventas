"""
Paquete de análisis de ventas profesional y escalable.

Este paquete proporciona funcionalidades modulares para analizar datos de ventas,
generar estadísticas, crear visualizaciones y realizar análisis avanzados.
"""

from ventas_analytics.config import ConfiguracionVisualizacion
from ventas_analytics.data import DataLoader
from ventas_analytics.statistics import EstadisticasVentas
from ventas_analytics.visualization import VisualizadorVentas
from ventas_analytics.reporting import PresentadorReporte
from ventas_analytics.advanced import AnalizadorAvanzado
from ventas_analytics.export import ExportadorDatos

__version__ = "1.0.0"
__all__ = [
    "ConfiguracionVisualizacion",
    "DataLoader",
    "EstadisticasVentas",
    "VisualizadorVentas",
    "PresentadorReporte",
    "AnalizadorAvanzado",
    "ExportadorDatos",
]

# Configurar logging básico si no está configurado
import logging

if not logging.getLogger().handlers:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

