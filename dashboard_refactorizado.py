"""
Dashboard interactivo para análisis de ventas.

Este script proporciona una interfaz interactiva para realizar análisis de ventas
utilizando el paquete ventas_analytics.
"""

import logging
from pathlib import Path

import matplotlib.pyplot as plt

from ventas_analytics import (
    DataLoader,
    EstadisticasVentas,
    VisualizadorVentas,
    PresentadorReporte,
    AnalizadorAvanzado,
    ExportadorDatos,
    ConfiguracionVisualizacion
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DashboardVentas:
    """Dashboard interactivo para análisis de ventas."""
    
    def __init__(self, archivo_datos: str):
        """
        Inicializar el dashboard.
        
        Args:
            archivo_datos: Ruta al archivo CSV con datos de ventas.
        """
        self.archivo_datos = archivo_datos
        self.loader = DataLoader(archivo_datos)
        self.config = ConfiguracionVisualizacion()
        self.visualizador = VisualizadorVentas(self.config)
        self._datos = None
        self._estadisticas = None
        self._analizador_avanzado = None
    
    def _cargar_datos(self):
        """Cargar y preparar datos."""
        if self._datos is None:
            self._datos = self.loader.cargar()
            # Preparar para análisis avanzado
            if 'dia_semana' not in self._datos.columns:
                self._datos['dia_semana'] = self._datos['fecha'].dt.day_name()
            if 'mes' not in self._datos.columns:
                self._datos['mes'] = self._datos['fecha'].dt.month
    
    @property
    def datos(self):
        """Obtener datos cargados."""
        self._cargar_datos()
        return self._datos
    
    @property
    def estadisticas(self):
        """Obtener estadísticas."""
        if self._estadisticas is None:
            self._estadisticas = EstadisticasVentas(self.datos)
        return self._estadisticas
    
    @property
    def analizador_avanzado(self):
        """Obtener analizador avanzado."""
        if self._analizador_avanzado is None:
            self._analizador_avanzado = AnalizadorAvanzado(self.datos, self.config)
        return self._analizador_avanzado
    
    def mostrar_menu(self):
        """Mostrar menú principal."""
        print("\n" + "=" * 60)
        print("🎯 DASHBOARD DE ANÁLISIS DE VENTAS")
        print("=" * 60)
        print("1. 📊 Resumen estadístico básico")
        print("2. 📈 Análisis de tendencias")
        print("3. 📅 Análisis de estacionalidad")
        print("4. 🔗 Análisis de correlaciones")
        print("5. 🔍 Detección de outliers")
        print("6. 🔮 Predicciones")
        print("7. 📋 Reporte completo básico")
        print("8. 📋 Reporte completo avanzado")
        print("9. 🎨 Visualizaciones personalizadas")
        print("10. 💾 Exportar datos procesados")
        print("0. 🚪 Salir")
        print("=" * 60)
    
    def resumen_basico(self):
        """Mostrar resumen estadístico básico."""
        print("\n" + "=" * 50)
        print("📊 RESUMEN ESTADÍSTICO BÁSICO")
        print("=" * 50)
        
        resumen = self.estadisticas.obtener_resumen_general()
        formatear = PresentadorReporte.formatear_moneda
        
        print(f"💰 Total de ventas: {formatear(resumen['total_ventas'])}")
        print(f"📊 Promedio por transacción: {formatear(resumen['promedio_ventas'])}")
        print(f"⬆️ Venta máxima: {formatear(resumen['venta_maxima'])}")
        print(f"⬇️ Venta mínima: {formatear(resumen['venta_minima'])}")
        print(f"📦 Total de productos vendidos: {resumen['total_productos_vendidos']:,}")
        
        # Top 3 productos por ventas
        print("\n🏆 TOP 3 PRODUCTOS POR VENTAS:")
        top_productos = self.estadisticas.obtener_ventas_por_producto().head(3)
        for i, (producto, venta) in enumerate(top_productos.items(), 1):
            print(f"  {i}. {producto}: {formatear(venta)}")
    
    def analizar_tendencias(self):
        """Análisis de tendencias."""
        print("\n" + "=" * 50)
        print("📈 ANÁLISIS DE TENDENCIAS")
        print("=" * 50)
        
        tendencia = self.analizador_avanzado.analizar_tendencias()
        print(f"📊 Pendiente: {tendencia['pendiente']:.2f}")
        print(f"🔗 R²: {tendencia['r_cuadrado']:.4f}")
        print(f"📈 Valor p: {tendencia['valor_p']:.4f}")
        
        if tendencia['pendiente'] > 0:
            print("📈 Tendencia: CRECIENTE")
        elif tendencia['pendiente'] < 0:
            print("📉 Tendencia: DECRECIENTE")
        else:
            print("➡️ Tendencia: ESTABLE")
        
        self.analizador_avanzado.graficar_tendencia(mostrar=True)
    
    def analizar_estacionalidad(self):
        """Análisis de estacionalidad."""
        print("\n" + "=" * 50)
        print("📅 ANÁLISIS DE ESTACIONALIDAD")
        print("=" * 50)
        
        ventas_dia = self.analizador_avanzado.obtener_ventas_por_dia_semana()
        print("📅 Ventas por día de la semana:")
        for dia, venta in ventas_dia.items():
            print(f"  {dia}: ${venta:,.2f}")
        
        self.analizador_avanzado.graficar_estacionalidad_semanal(mostrar=True)
    
    def analizar_correlaciones(self):
        """Análisis de correlaciones."""
        print("\n" + "=" * 50)
        print("🔗 ANÁLISIS DE CORRELACIONES")
        print("=" * 50)
        
        correlaciones = self.analizador_avanzado.analizar_correlaciones()
        print("Matriz de correlaciones:")
        print(correlaciones)
        
        self.analizador_avanzado.graficar_correlaciones(mostrar=True)
    
    def detectar_outliers(self):
        """Detección de outliers."""
        print("\n" + "=" * 50)
        print("🔍 DETECCIÓN DE OUTLIERS")
        print("=" * 50)
        
        outliers, limites = self.analizador_avanzado.detectar_outliers()
        print(f"📊 Límite inferior: ${limites['limite_inferior']:.2f}")
        print(f"📊 Límite superior: ${limites['limite_superior']:.2f}")
        print(f"🔍 Outliers detectados: {len(outliers)}")
        
        if len(outliers) > 0:
            print("\n⚠️ Outliers encontrados:")
            for _, row in outliers.iterrows():
                print(f"  {row['fecha'].strftime('%Y-%m-%d')} - {row['producto']}: ${row['ventas']:.2f}")
        else:
            print("✅ No se detectaron outliers")
        
        self.analizador_avanzado.graficar_outliers(mostrar=True)
    
    def hacer_predicciones(self):
        """Realizar predicciones."""
        print("\n" + "=" * 50)
        print("🔮 PREDICCIONES")
        print("=" * 50)
        
        predicciones = self.analizador_avanzado.predecir_ventas(dias_futuros=5)
        print("🔮 Predicciones para los próximos 5 días:")
        for _, row in predicciones.iterrows():
            print(f"  {row['fecha'].strftime('%Y-%m-%d')}: ${row['prediccion']:.2f}")
        
        self.analizador_avanzado.graficar_predicciones(mostrar=True)
    
    def reporte_completo_basico(self):
        """Generar reporte completo básico."""
        print("\n" + "=" * 60)
        print("📋 GENERANDO REPORTE COMPLETO BÁSICO")
        print("=" * 60)
        
        PresentadorReporte.mostrar_resumen_estadistico(self.estadisticas)
        print("\n✅ Reporte básico completo generado!")
    
    def reporte_completo_avanzado(self):
        """Generar reporte completo avanzado."""
        print("\n" + "=" * 60)
        print("📋 GENERANDO REPORTE COMPLETO AVANZADO")
        print("=" * 60)
        
        self.resumen_basico()
        self.analizar_tendencias()
        self.analizar_estacionalidad()
        self.analizar_correlaciones()
        self.detectar_outliers()
        self.hacer_predicciones()
        
        print("\n✅ Reporte avanzado completo generado!")
    
    def visualizaciones_personalizadas(self):
        """Visualizaciones personalizadas."""
        print("\n" + "=" * 50)
        print("🎨 VISUALIZACIONES PERSONALIZADAS")
        print("=" * 50)
        
        # Crear subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Ventas por categoría
        ventas_cat = self.estadisticas.obtener_ventas_por_categoria()
        ax1.pie(ventas_cat.values, labels=ventas_cat.index, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Distribución por Categoría')
        
        # 2. Ventas por región
        ventas_reg = self.estadisticas.obtener_ventas_por_region()
        bars = ax2.bar(ventas_reg.index, ventas_reg.values, color='skyblue')
        ax2.set_title('Ventas por Región')
        ax2.set_ylabel('Ventas ($)')
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'${height:,.0f}', ha='center', va='bottom')
        
        # 3. Evolución temporal
        ventas_temp = self.estadisticas.obtener_evolucion_temporal()
        ax3.plot(ventas_temp['fecha'], ventas_temp['ventas'], marker='o')
        ax3.set_title('Evolución Temporal')
        ax3.set_ylabel('Ventas ($)')
        ax3.tick_params(axis='x', rotation=45)
        
        # 4. Productos más vendidos
        prod_ventas = self.estadisticas.obtener_productos_mas_vendidos().sort_values(ascending=True)
        bars = ax4.barh(prod_ventas.index, prod_ventas.values, color='lightcoral')
        ax4.set_title('Productos Más Vendidos')
        ax4.set_xlabel('Cantidad')
        
        plt.tight_layout()
        plt.show()
    
    def exportar_datos(self):
        """Exportar datos procesados."""
        print("\n" + "=" * 50)
        print("💾 EXPORTAR DATOS PROCESADOS")
        print("=" * 50)
        
        exportador = ExportadorDatos(self.estadisticas)
        ruta = exportador.exportar_excel()
        
        print(f"✅ Datos exportados a '{ruta}'")
        print("📊 Hojas incluidas:")
        print("  - Datos_Originales")
        print("  - Resumen_Categoria")
        print("  - Resumen_Region")
        print("  - Resumen_Producto")
    
    def ejecutar(self):
        """Ejecutar el dashboard."""
        try:
            # Cargar datos al inicio
            self._cargar_datos()
            print(f"✅ Datos cargados exitosamente: {len(self.datos)} registros")
        except Exception as e:
            print(f"❌ Error al cargar datos: {e}")
            return
        
        while True:
            self.mostrar_menu()
            opcion = input("\nSelecciona una opción (0-10): ").strip()
            
            try:
                if opcion == '1':
                    self.resumen_basico()
                elif opcion == '2':
                    self.analizar_tendencias()
                elif opcion == '3':
                    self.analizar_estacionalidad()
                elif opcion == '4':
                    self.analizar_correlaciones()
                elif opcion == '5':
                    self.detectar_outliers()
                elif opcion == '6':
                    self.hacer_predicciones()
                elif opcion == '7':
                    self.reporte_completo_basico()
                elif opcion == '8':
                    self.reporte_completo_avanzado()
                elif opcion == '9':
                    self.visualizaciones_personalizadas()
                elif opcion == '10':
                    self.exportar_datos()
                elif opcion == '0':
                    print("\n👋 ¡Gracias por usar el Dashboard de Análisis de Ventas!")
                    break
                else:
                    print("❌ Opción no válida. Por favor, selecciona una opción del 0 al 10.")
            except Exception as e:
                logger.error(f"Error al ejecutar opción {opcion}: {e}", exc_info=True)
                print(f"❌ Error: {e}")
            
            input("\nPresiona Enter para continuar...")


def main():
    """Función principal."""
    print("🎯 DASHBOARD INTERACTIVO DE ANÁLISIS DE VENTAS")
    print("=" * 60)
    
    try:
        dashboard = DashboardVentas('datos_ventas.csv')
        dashboard.ejecutar()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido por el usuario. ¡Hasta luego!")
    except Exception as e:
        logger.error(f"Error fatal: {e}", exc_info=True)
        print(f"❌ Error fatal: {e}")


if __name__ == "__main__":
    main()

