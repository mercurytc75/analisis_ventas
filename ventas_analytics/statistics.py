"""
Módulo para cálculo de estadísticas de ventas.
"""

from typing import Dict, Optional

import pandas as pd


class EstadisticasVentas:
    """Clase responsable de calcular estadísticas de ventas."""
    
    def __init__(self, datos: pd.DataFrame):
        """
        Inicializar el calculador de estadísticas.
        
        Args:
            datos: DataFrame con los datos de ventas.
        """
        self.datos = datos
        self._validar_datos()
    
    def _validar_datos(self) -> None:
        """Validar que los datos son válidos para análisis."""
        if self.datos.empty:
            raise ValueError("No hay datos para analizar")
    
    def obtener_resumen_general(self) -> Dict[str, float]:
        """
        Obtener resumen estadístico general.
        
        Returns:
            Diccionario con estadísticas clave.
        """
        return {
            'total_ventas': float(self.datos['ventas'].sum()),
            'promedio_ventas': float(self.datos['ventas'].mean()),
            'mediana_ventas': float(self.datos['ventas'].median()),
            'venta_maxima': float(self.datos['ventas'].max()),
            'venta_minima': float(self.datos['ventas'].min()),
            'desviacion_estandar': float(self.datos['ventas'].std()),
            'total_productos_vendidos': int(self.datos['cantidad'].sum()),
            'promedio_cantidad': float(self.datos['cantidad'].mean()),
        }
    
    def obtener_ventas_por_categoria(self) -> pd.Series:
        """
        Calcular ventas totales por categoría.
        
        Returns:
            Series con ventas agrupadas por categoría, ordenadas descendente.
        """
        return self.datos.groupby('categoria')['ventas'].sum().sort_values(ascending=False)
    
    def obtener_ventas_por_region(self) -> pd.Series:
        """
        Calcular ventas totales por región.
        
        Returns:
            Series con ventas agrupadas por región, ordenadas descendente.
        """
        return self.datos.groupby('region')['ventas'].sum().sort_values(ascending=False)
    
    def obtener_productos_mas_vendidos(self, top_n: Optional[int] = None) -> pd.Series:
        """
        Obtener productos más vendidos por cantidad.
        
        Args:
            top_n: Número de productos a retornar. Si es None, retorna todos.
            
        Returns:
            Series con cantidad vendida por producto, ordenada descendente.
        """
        productos = self.datos.groupby('producto')['cantidad'].sum().sort_values(ascending=False)
        if top_n:
            productos = productos.head(top_n)
        return productos
    
    def obtener_evolucion_temporal(self) -> pd.DataFrame:
        """
        Calcular evolución de ventas en el tiempo.
        
        Returns:
            DataFrame con fecha y ventas diarias totales.
        """
        return self.datos.groupby('fecha')['ventas'].sum().reset_index()
    
    def obtener_ventas_por_producto(self) -> pd.Series:
        """
        Calcular ventas totales por producto.
        
        Returns:
            Series con ventas agrupadas por producto, ordenadas descendente.
        """
        return self.datos.groupby('producto')['ventas'].sum().sort_values(ascending=False)

