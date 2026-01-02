"""
Módulo para exportación de datos y reportes.
"""

from pathlib import Path
from typing import Optional

import pandas as pd

from ventas_analytics.statistics import EstadisticasVentas

import logging
logger = logging.getLogger(__name__)


class ExportadorDatos:
    """Clase para exportar datos procesados a diferentes formatos."""
    
    def __init__(self, estadisticas: EstadisticasVentas):
        """
        Inicializar el exportador.
        
        Args:
            estadisticas: Instancia de EstadisticasVentas con los datos a exportar.
        """
        self.estadisticas = estadisticas
        self.datos = estadisticas.datos
    
    def exportar_excel(
        self,
        nombre_archivo: str = 'reporte_ventas.xlsx',
        directorio: str = "."
    ) -> Path:
        """
        Exportar datos procesados a Excel.
        
        Args:
            nombre_archivo: Nombre del archivo Excel.
            directorio: Directorio donde guardar el archivo.
            
        Returns:
            Path al archivo creado.
        """
        directorio_path = Path(directorio)
        directorio_path.mkdir(parents=True, exist_ok=True)
        ruta_completa = directorio_path / nombre_archivo
        
        # Crear resúmenes
        resumen_categoria = self.datos.groupby('categoria').agg({
            'ventas': ['sum', 'mean', 'count'],
            'cantidad': 'sum'
        }).round(2)
        
        resumen_region = self.datos.groupby('region').agg({
            'ventas': ['sum', 'mean', 'count'],
            'cantidad': 'sum'
        }).round(2)
        
        resumen_producto = self.datos.groupby('producto').agg({
            'ventas': ['sum', 'mean'],
            'cantidad': 'sum'
        }).round(2)
        
        # Exportar a Excel
        with pd.ExcelWriter(ruta_completa) as writer:
            self.datos.to_excel(writer, sheet_name='Datos_Originales', index=False)
            resumen_categoria.to_excel(writer, sheet_name='Resumen_Categoria')
            resumen_region.to_excel(writer, sheet_name='Resumen_Region')
            resumen_producto.to_excel(writer, sheet_name='Resumen_Producto')
        
        logger.info(f"Datos exportados a: {ruta_completa}")
        return ruta_completa
    
    def exportar_csv(
        self,
        nombre_archivo: str = 'datos_procesados.csv',
        directorio: str = "."
    ) -> Path:
        """
        Exportar datos a CSV.
        
        Args:
            nombre_archivo: Nombre del archivo CSV.
            directorio: Directorio donde guardar el archivo.
            
        Returns:
            Path al archivo creado.
        """
        directorio_path = Path(directorio)
        directorio_path.mkdir(parents=True, exist_ok=True)
        ruta_completa = directorio_path / nombre_archivo
        
        self.datos.to_csv(ruta_completa, index=False)
        logger.info(f"Datos exportados a: {ruta_completa}")
        return ruta_completa

