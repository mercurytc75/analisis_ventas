import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np

# Configurar el estilo de las gráficas
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class AnalizadorVentas:
    def __init__(self, archivo_datos):
        """Inicializar el analizador con el archivo de datos"""
        self.archivo_datos = archivo_datos
        self.datos = None
        self.cargar_datos()
    
    def cargar_datos(self):
        """Cargar los datos desde el archivo CSV"""
        try:
            self.datos = pd.read_csv(self.archivo_datos)
            self.datos['fecha'] = pd.to_datetime(self.datos['fecha'])
            print(f"✅ Datos cargados exitosamente: {len(self.datos)} registros")
        except Exception as e:
            print(f"❌ Error al cargar datos: {e}")
    
    def mostrar_resumen_estadistico(self):
        """Mostrar un resumen estadístico de las ventas"""
        print("\n" + "="*50)
        print("📊 RESUMEN ESTADÍSTICO DE VENTAS")
        print("="*50)
        
        # Estadísticas generales
        print(f"Total de ventas: ${self.datos['ventas'].sum():,.2f}")
        print(f"Promedio de ventas por transacción: ${self.datos['ventas'].mean():,.2f}")
        print(f"Venta máxima: ${self.datos['ventas'].max():,.2f}")
        print(f"Venta mínima: ${self.datos['ventas'].min():,.2f}")
        print(f"Total de productos vendidos: {self.datos['cantidad'].sum()}")
        
        # Ventas por categoría
        print("\n📈 VENTAS POR CATEGORÍA:")
        ventas_categoria = self.datos.groupby('categoria')['ventas'].sum().sort_values(ascending=False)
        for categoria, venta in ventas_categoria.items():
            print(f"  {categoria}: ${venta:,.2f}")
        
        # Ventas por región
        print("\n🌍 VENTAS POR REGIÓN:")
        ventas_region = self.datos.groupby('region')['ventas'].sum().sort_values(ascending=False)
        for region, venta in ventas_region.items():
            print(f"  {region}: ${venta:,.2f}")
    
    def graficar_ventas_por_categoria(self):
        """Crear gráfica de ventas por categoría"""
        plt.figure(figsize=(10, 6))
        ventas_categoria = self.datos.groupby('categoria')['ventas'].sum().sort_values(ascending=False)
        
        bars = plt.bar(ventas_categoria.index, ventas_categoria.values, color='skyblue', edgecolor='navy')
        plt.title('Ventas Totales por Categoría', fontsize=16, fontweight='bold')
        plt.xlabel('Categoría', fontsize=12)
        plt.ylabel('Ventas ($)', fontsize=12)
        plt.xticks(rotation=45)
        
        # Agregar valores en las barras
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'${height:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('ventas_por_categoria.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def graficar_ventas_por_region(self):
        """Crear gráfica de ventas por región"""
        plt.figure(figsize=(10, 6))
        ventas_region = self.datos.groupby('region')['ventas'].sum().sort_values(ascending=False)
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        # Crear explode dinámicamente basado en la cantidad de regiones
        explode = [0.05] * len(ventas_region)
        plt.pie(ventas_region.values, labels=ventas_region.index, autopct='%1.1f%%', 
                colors=colors[:len(ventas_region)], startangle=90, explode=explode)
        plt.title('Distribución de Ventas por Región', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('ventas_por_region.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def graficar_evolucion_ventas(self):
        """Crear gráfica de evolución de ventas en el tiempo"""
        plt.figure(figsize=(12, 6))
        
        # Agrupar ventas por fecha
        ventas_diarias = self.datos.groupby('fecha')['ventas'].sum().reset_index()
        
        plt.plot(ventas_diarias['fecha'], ventas_diarias['ventas'], 
                marker='o', linewidth=2, markersize=6, color='#2E86AB')
        plt.title('Evolución de Ventas Diarias', fontsize=16, fontweight='bold')
        plt.xlabel('Fecha', fontsize=12)
        plt.ylabel('Ventas ($)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig('evolucion_ventas.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def graficar_productos_mas_vendidos(self):
        """Crear gráfica de productos más vendidos"""
        plt.figure(figsize=(10, 6))
        productos_ventas = self.datos.groupby('producto')['cantidad'].sum().sort_values(ascending=True)
        
        bars = plt.barh(productos_ventas.index, productos_ventas.values, color='lightcoral')
        plt.title('Productos Más Vendidos (por cantidad)', fontsize=16, fontweight='bold')
        plt.xlabel('Cantidad Vendida', fontsize=12)
        plt.ylabel('Producto', fontsize=12)
        
        # Agregar valores en las barras
        for i, bar in enumerate(bars):
            width = bar.get_width()
            plt.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                    str(int(width)), ha='left', va='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('productos_mas_vendidos.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def generar_reporte_completo(self):
        """Generar un reporte completo con todas las visualizaciones"""
        print("\n" + "="*60)
        print("🚀 GENERANDO REPORTE COMPLETO DE ANÁLISIS DE VENTAS")
        print("="*60)
        
        # Mostrar resumen estadístico
        self.mostrar_resumen_estadistico()
        
        # Generar todas las gráficas
        print("\n📊 Generando visualizaciones...")
        self.graficar_ventas_por_categoria()
        self.graficar_ventas_por_region()
        self.graficar_evolucion_ventas()
        self.graficar_productos_mas_vendidos()
        
        print("\n✅ Reporte completo generado exitosamente!")
        print("📁 Las gráficas se han guardado como archivos PNG en el directorio actual.")

def main():
    """Función principal del programa"""
    print("🎯 ANÁLISIS DE VENTAS - HERRAMIENTA DE ANÁLISIS")
    print("="*50)
    
    # Crear instancia del analizador
    analizador = AnalizadorVentas('datos_ventas.csv')
    
    # Generar reporte completo
    analizador.generar_reporte_completo()

if __name__ == "__main__":
    main() 