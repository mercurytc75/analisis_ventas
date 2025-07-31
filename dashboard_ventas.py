import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta
from scipy import stats

class DashboardVentas:
    def __init__(self, archivo_datos):
        """Inicializar el dashboard"""
        self.archivo_datos = archivo_datos
        self.datos = None
        self.cargar_datos()
    
    def cargar_datos(self):
        """Cargar y preparar los datos"""
        try:
            self.datos = pd.read_csv(self.archivo_datos)
            self.datos['fecha'] = pd.to_datetime(self.datos['fecha'])
            self.datos['dia_semana'] = self.datos['fecha'].dt.day_name()
            self.datos['mes'] = self.datos['fecha'].dt.month
            print(f"✅ Datos cargados exitosamente: {len(self.datos)} registros")
        except Exception as e:
            print(f"❌ Error al cargar datos: {e}")
    
    def mostrar_menu(self):
        """Mostrar menú principal"""
        print("\n" + "="*60)
        print("🎯 DASHBOARD DE ANÁLISIS DE VENTAS")
        print("="*60)
        print("1. 📊 Resumen estadístico básico")
        print("2. 📈 Análisis de tendencias")
        print("3. 📅 Análisis de estacionalidad")
        print("4. 🔗 Análisis de correlaciones")
        print("5. 🔍 Detección de outliers")
        print("6. 🔮 Predicciones")
        print("7. 📋 Reporte completo")
        print("8. 🎨 Visualizaciones personalizadas")
        print("9. 💾 Exportar datos procesados")
        print("0. 🚪 Salir")
        print("="*60)
    
    def resumen_basico(self):
        """Mostrar resumen estadístico básico"""
        print("\n" + "="*50)
        print("📊 RESUMEN ESTADÍSTICO BÁSICO")
        print("="*50)
        
        total_ventas = self.datos['ventas'].sum()
        promedio_ventas = self.datos['ventas'].mean()
        max_venta = self.datos['ventas'].max()
        min_venta = self.datos['ventas'].min()
        total_productos = self.datos['cantidad'].sum()
        
        print(f"💰 Total de ventas: ${total_ventas:,.2f}")
        print(f"📊 Promedio por transacción: ${promedio_ventas:,.2f}")
        print(f"⬆️ Venta máxima: ${max_venta:,.2f}")
        print(f"⬇️ Venta mínima: ${min_venta:,.2f}")
        print(f"📦 Total de productos vendidos: {total_productos}")
        
        # Top 3 productos por ventas
        print("\n🏆 TOP 3 PRODUCTOS POR VENTAS:")
        top_productos = self.datos.groupby('producto')['ventas'].sum().sort_values(ascending=False).head(3)
        for i, (producto, venta) in enumerate(top_productos.items(), 1):
            print(f"  {i}. {producto}: ${venta:,.2f}")
    
    def analizar_tendencias(self):
        """Análisis de tendencias"""
        print("\n" + "="*50)
        print("📈 ANÁLISIS DE TENDENCIAS")
        print("="*50)
        
        ventas_diarias = self.datos.groupby('fecha')['ventas'].sum().reset_index()
        x = np.arange(len(ventas_diarias))
        y = ventas_diarias['ventas'].values
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        print(f"📊 Pendiente: {slope:.2f}")
        print(f"🔗 R²: {r_value**2:.4f}")
        print(f"📈 Valor p: {p_value:.4f}")
        
        if slope > 0:
            print("📈 Tendencia: CRECIENTE")
        elif slope < 0:
            print("📉 Tendencia: DECRECIENTE")
        else:
            print("➡️ Tendencia: ESTABLE")
        
        # Graficar
        plt.figure(figsize=(12, 6))
        plt.plot(ventas_diarias['fecha'], ventas_diarias['ventas'], 
                marker='o', linewidth=2, markersize=6, label='Ventas reales')
        trend_line = slope * x + intercept
        plt.plot(ventas_diarias['fecha'], trend_line, 'r--', linewidth=2, label='Tendencia')
        
        plt.title('Análisis de Tendencia de Ventas', fontsize=16, fontweight='bold')
        plt.xlabel('Fecha', fontsize=12)
        plt.ylabel('Ventas ($)', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    def analizar_estacionalidad(self):
        """Análisis de estacionalidad"""
        print("\n" + "="*50)
        print("📅 ANÁLISIS DE ESTACIONALIDAD")
        print("="*50)
        
        # Por día de la semana
        ventas_dia = self.datos.groupby('dia_semana')['ventas'].sum().reindex([
            'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
        ])
        
        print("📅 Ventas por día de la semana:")
        for dia, venta in ventas_dia.items():
            print(f"  {dia}: ${venta:,.2f}")
        
        # Graficar
        plt.figure(figsize=(10, 6))
        bars = plt.bar(ventas_dia.index, ventas_dia.values, color='lightgreen')
        plt.title('Ventas por Día de la Semana', fontsize=16, fontweight='bold')
        plt.xlabel('Día de la Semana', fontsize=12)
        plt.ylabel('Ventas ($)', fontsize=12)
        plt.xticks(rotation=45)
        
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'${height:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.show()
    
    def analizar_correlaciones(self):
        """Análisis de correlaciones"""
        print("\n" + "="*50)
        print("🔗 ANÁLISIS DE CORRELACIONES")
        print("="*50)
        
        datos_corr = self.datos.copy()
        datos_corr['categoria_num'] = pd.Categorical(datos_corr['categoria']).codes
        datos_corr['region_num'] = pd.Categorical(datos_corr['region']).codes
        
        correlaciones = datos_corr[['ventas', 'cantidad', 'categoria_num', 'region_num']].corr()
        
        print("Matriz de correlaciones:")
        print(correlaciones)
        
        # Graficar
        plt.figure(figsize=(8, 6))
        sns.heatmap(correlaciones, annot=True, cmap='coolwarm', center=0, 
                   square=True, linewidths=0.5)
        plt.title('Matriz de Correlaciones', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def detectar_outliers(self):
        """Detección de outliers"""
        print("\n" + "="*50)
        print("🔍 DETECCIÓN DE OUTLIERS")
        print("="*50)
        
        Q1 = self.datos['ventas'].quantile(0.25)
        Q3 = self.datos['ventas'].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = self.datos[(self.datos['ventas'] < lower_bound) | 
                             (self.datos['ventas'] > upper_bound)]
        
        print(f"📊 Límite inferior: ${lower_bound:.2f}")
        print(f"📊 Límite superior: ${upper_bound:.2f}")
        print(f"🔍 Outliers detectados: {len(outliers)}")
        
        if len(outliers) > 0:
            print("\n⚠️ Outliers encontrados:")
            for _, row in outliers.iterrows():
                print(f"  {row['fecha'].strftime('%Y-%m-%d')} - {row['producto']}: ${row['ventas']:.2f}")
        else:
            print("✅ No se detectaron outliers")
        
        # Graficar
        plt.figure(figsize=(10, 6))
        plt.boxplot(self.datos['ventas'], patch_artist=True, 
                   boxprops=dict(facecolor='lightblue'))
        plt.title('Distribución de Ventas (Boxplot)', fontsize=16, fontweight='bold')
        plt.ylabel('Ventas ($)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def hacer_predicciones(self):
        """Realizar predicciones"""
        print("\n" + "="*50)
        print("🔮 PREDICCIONES")
        print("="*50)
        
        ventas_diarias = self.datos.groupby('fecha')['ventas'].sum().reset_index()
        x = np.arange(len(ventas_diarias))
        y = ventas_diarias['ventas'].values
        
        slope, intercept, _, _, _ = stats.linregress(x, y)
        
        # Predecir próximos 5 días
        ultima_fecha = ventas_diarias['fecha'].max()
        predicciones = []
        fechas_pred = []
        
        for i in range(1, 6):
            fecha_pred = ultima_fecha + timedelta(days=i)
            pred = slope * (len(ventas_diarias) + i - 1) + intercept
            predicciones.append(max(0, pred))
            fechas_pred.append(fecha_pred)
        
        print("🔮 Predicciones para los próximos 5 días:")
        for fecha, pred in zip(fechas_pred, predicciones):
            print(f"  {fecha.strftime('%Y-%m-%d')}: ${pred:.2f}")
        
        # Graficar
        plt.figure(figsize=(12, 6))
        plt.plot(ventas_diarias['fecha'], ventas_diarias['ventas'], 
                marker='o', linewidth=2, markersize=6, label='Ventas reales')
        plt.plot(fechas_pred, predicciones, 'r--', marker='s', 
                linewidth=2, markersize=6, label='Predicciones')
        
        plt.title('Predicción de Ventas (Próximos 5 días)', fontsize=16, fontweight='bold')
        plt.xlabel('Fecha', fontsize=12)
        plt.ylabel('Ventas ($)', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    def reporte_completo(self):
        """Generar reporte completo"""
        print("\n" + "="*60)
        print("📋 GENERANDO REPORTE COMPLETO")
        print("="*60)
        
        self.resumen_basico()
        self.analizar_tendencias()
        self.analizar_estacionalidad()
        self.analizar_correlaciones()
        self.detectar_outliers()
        self.hacer_predicciones()
        
        print("\n✅ Reporte completo generado!")
    
    def visualizaciones_personalizadas(self):
        """Visualizaciones personalizadas"""
        print("\n" + "="*50)
        print("🎨 VISUALIZACIONES PERSONALIZADAS")
        print("="*50)
        
        # Crear subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # 1. Ventas por categoría
        ventas_cat = self.datos.groupby('categoria')['ventas'].sum()
        ax1.pie(ventas_cat.values, labels=ventas_cat.index, autopct='%1.1f%%', startangle=90)
        ax1.set_title('Distribución por Categoría')
        
        # 2. Ventas por región
        ventas_reg = self.datos.groupby('region')['ventas'].sum()
        bars = ax2.bar(ventas_reg.index, ventas_reg.values, color='skyblue')
        ax2.set_title('Ventas por Región')
        ax2.set_ylabel('Ventas ($)')
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'${height:,.0f}', ha='center', va='bottom')
        
        # 3. Evolución temporal
        ventas_temp = self.datos.groupby('fecha')['ventas'].sum()
        ax3.plot(ventas_temp.index, ventas_temp.values, marker='o')
        ax3.set_title('Evolución Temporal')
        ax3.set_ylabel('Ventas ($)')
        ax3.tick_params(axis='x', rotation=45)
        
        # 4. Productos más vendidos
        prod_ventas = self.datos.groupby('producto')['cantidad'].sum().sort_values(ascending=True)
        bars = ax4.barh(prod_ventas.index, prod_ventas.values, color='lightcoral')
        ax4.set_title('Productos Más Vendidos')
        ax4.set_xlabel('Cantidad')
        
        plt.tight_layout()
        plt.show()
    
    def exportar_datos(self):
        """Exportar datos procesados"""
        print("\n" + "="*50)
        print("💾 EXPORTAR DATOS PROCESADOS")
        print("="*50)
        
        # Crear resumen de datos
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
        with pd.ExcelWriter('reporte_ventas.xlsx') as writer:
            self.datos.to_excel(writer, sheet_name='Datos_Originales', index=False)
            resumen_categoria.to_excel(writer, sheet_name='Resumen_Categoria')
            resumen_region.to_excel(writer, sheet_name='Resumen_Region')
            resumen_producto.to_excel(writer, sheet_name='Resumen_Producto')
        
        print("✅ Datos exportados a 'reporte_ventas.xlsx'")
        print("📊 Hojas incluidas:")
        print("  - Datos_Originales")
        print("  - Resumen_Categoria")
        print("  - Resumen_Region")
        print("  - Resumen_Producto")
    
    def ejecutar(self):
        """Ejecutar el dashboard"""
        while True:
            self.mostrar_menu()
            opcion = input("\nSelecciona una opción (0-9): ").strip()
            
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
                self.reporte_completo()
            elif opcion == '8':
                self.visualizaciones_personalizadas()
            elif opcion == '9':
                self.exportar_datos()
            elif opcion == '0':
                print("\n👋 ¡Gracias por usar el Dashboard de Análisis de Ventas!")
                break
            else:
                print("❌ Opción no válida. Por favor, selecciona una opción del 0 al 9.")
            
            input("\nPresiona Enter para continuar...")

def main():
    """Función principal"""
    print("🎯 DASHBOARD INTERACTIVO DE ANÁLISIS DE VENTAS")
    print("="*60)
    
    dashboard = DashboardVentas('datos_ventas.csv')
    dashboard.ejecutar()

if __name__ == "__main__":
    main() 