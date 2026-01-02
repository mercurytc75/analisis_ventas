"""
Módulo para presentación de reportes.
"""

from ventas_analytics.statistics import EstadisticasVentas


class PresentadorReporte:
    """Clase responsable de presentar reportes en formato legible."""
    
    @staticmethod
    def formatear_moneda(valor: float) -> str:
        """
        Formatear valor como moneda.
        
        Args:
            valor: Valor numérico a formatear.
            
        Returns:
            String formateado como moneda.
        """
        return f"${valor:,.2f}"
    
    @staticmethod
    def mostrar_resumen_estadistico(estadisticas: EstadisticasVentas) -> None:
        """
        Mostrar resumen estadístico en consola.
        
        Args:
            estadisticas: Instancia de EstadisticasVentas.
        """
        print("\n" + "=" * 50)
        print("📊 RESUMEN ESTADÍSTICO DE VENTAS")
        print("=" * 50)
        
        resumen = estadisticas.obtener_resumen_general()
        formatear = PresentadorReporte.formatear_moneda
        
        print(f"Total de ventas: {formatear(resumen['total_ventas'])}")
        print(f"Promedio de ventas por transacción: {formatear(resumen['promedio_ventas'])}")
        print(f"Mediana de ventas: {formatear(resumen['mediana_ventas'])}")
        print(f"Venta máxima: {formatear(resumen['venta_maxima'])}")
        print(f"Venta mínima: {formatear(resumen['venta_minima'])}")
        print(f"Desviación estándar: {formatear(resumen['desviacion_estandar'])}")
        print(f"Total de productos vendidos: {resumen['total_productos_vendidos']:,}")
        print(f"Promedio de cantidad por transacción: {resumen['promedio_cantidad']:.2f}")
        
        # Ventas por categoría
        print("\n📈 VENTAS POR CATEGORÍA:")
        ventas_categoria = estadisticas.obtener_ventas_por_categoria()
        for categoria, venta in ventas_categoria.items():
            print(f"  {categoria}: {formatear(venta)}")
        
        # Ventas por región
        print("\n🌍 VENTAS POR REGIÓN:")
        ventas_region = estadisticas.obtener_ventas_por_region()
        for region, venta in ventas_region.items():
            print(f"  {region}: {formatear(venta)}")

