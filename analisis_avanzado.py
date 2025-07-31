import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta
from scipy import stats

class AnalizadorAvanzado:
    def __init__(self, archivo_datos):
        """Inicializar el analizador avanzado"""
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
    
    def analizar_tendencias(self):
        """Analizar tendencias en las ventas"""
        print("\n" + "="*50)
        print("📈 ANÁLISIS DE TENDENCIAS")
        print("="*50)
        
        # Agrupar por fecha y calcular ventas diarias
        ventas_diarias = self.datos.groupby('fecha')['ventas'].sum().reset_index()
        
        # Calcular tendencia lineal
        x = np.arange(len(ventas_diarias))
        y = ventas_diarias['ventas'].values
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        print(f"Pendiente de la tendencia: {slope:.2f}")
        print(f"Coeficiente de correlación (R²): {r_value**2:.4f}")
        print(f"Valor p: {p_value:.4f}")
        
        if slope > 0:
            print("📈 Tendencia: CRECIENTE")
        elif slope < 0:
            print("📉 Tendencia: DECRECIENTE")
        else:
            print("➡️ Tendencia: ESTABLE")
        
        # Graficar tendencia
        plt.figure(figsize=(12, 6))
        plt.plot(ventas_diarias['fecha'], ventas_diarias['ventas'], 
                marker='o', linewidth=2, markersize=6, label='Ventas reales')
        
        # Línea de tendencia
        trend_line = slope * x + intercept
        plt.plot(ventas_diarias['fecha'], trend_line, 'r--', linewidth=2, label='Tendencia')
        
        plt.title('Análisis de Tendencia de Ventas', fontsize=16, fontweight='bold')
        plt.xlabel('Fecha', fontsize=12)
        plt.ylabel('Ventas ($)', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig('tendencia_ventas.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def analizar_estacionalidad(self):
        """Analizar patrones estacionales"""
        print("\n" + "="*50)
        print("📅 ANÁLISIS DE ESTACIONALIDAD")
        print("="*50)
        
        # Ventas por día de la semana
        ventas_dia = self.datos.groupby('dia_semana')['ventas'].sum().reindex([
            'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
        ])
        
        print("Ventas por día de la semana:")
        for dia, venta in ventas_dia.items():
            print(f"  {dia}: ${venta:,.2f}")
        
        # Graficar estacionalidad semanal
        plt.figure(figsize=(10, 6))
        bars = plt.bar(ventas_dia.index, ventas_dia.values, color='lightgreen')
        plt.title('Ventas por Día de la Semana', fontsize=16, fontweight='bold')
        plt.xlabel('Día de la Semana', fontsize=12)
        plt.ylabel('Ventas ($)', fontsize=12)
        plt.xticks(rotation=45)
        
        # Agregar valores en las barras
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'${height:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('estacionalidad_semanal.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def analizar_correlaciones(self):
        """Analizar correlaciones entre variables"""
        print("\n" + "="*50)
        print("🔗 ANÁLISIS DE CORRELACIONES")
        print("="*50)
        
        # Crear variables numéricas para correlación
        datos_corr = self.datos.copy()
        datos_corr['categoria_num'] = pd.Categorical(datos_corr['categoria']).codes
        datos_corr['region_num'] = pd.Categorical(datos_corr['region']).codes
        
        # Calcular correlaciones
        correlaciones = datos_corr[['ventas', 'cantidad', 'categoria_num', 'region_num']].corr()
        
        print("Matriz de correlaciones:")
        print(correlaciones)
        
        # Graficar matriz de correlaciones
        plt.figure(figsize=(8, 6))
        sns.heatmap(correlaciones, annot=True, cmap='coolwarm', center=0, 
                   square=True, linewidths=0.5)
        plt.title('Matriz de Correlaciones', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('correlaciones.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def analizar_outliers(self):
        """Detectar y analizar outliers en las ventas"""
        print("\n" + "="*50)
        print("🔍 ANÁLISIS DE OUTLIERS")
        print("="*50)
        
        # Calcular estadísticas para detectar outliers
        Q1 = self.datos['ventas'].quantile(0.25)
        Q3 = self.datos['ventas'].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = self.datos[(self.datos['ventas'] < lower_bound) | 
                             (self.datos['ventas'] > upper_bound)]
        
        print(f"Límite inferior: ${lower_bound:.2f}")
        print(f"Límite superior: ${upper_bound:.2f}")
        print(f"Outliers detectados: {len(outliers)}")
        
        if len(outliers) > 0:
            print("\nOutliers encontrados:")
            for _, row in outliers.iterrows():
                print(f"  {row['fecha'].strftime('%Y-%m-%d')} - {row['producto']}: ${row['ventas']:.2f}")
        
        # Graficar boxplot
        plt.figure(figsize=(10, 6))
        plt.boxplot(self.datos['ventas'], patch_artist=True, 
                   boxprops=dict(facecolor='lightblue'))
        plt.title('Distribución de Ventas (Boxplot)', fontsize=16, fontweight='bold')
        plt.ylabel('Ventas ($)', fontsize=12)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('outliers_ventas.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def prediccion_simple(self):
        """Realizar predicción simple basada en tendencia"""
        print("\n" + "="*50)
        print("🔮 PREDICCIÓN SIMPLE")
        print("="*50)
        
        # Calcular tendencia
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
            predicciones.append(max(0, pred))  # No ventas negativas
            fechas_pred.append(fecha_pred)
        
        print("Predicciones para los próximos 5 días:")
        for fecha, pred in zip(fechas_pred, predicciones):
            print(f"  {fecha.strftime('%Y-%m-%d')}: ${pred:.2f}")
        
        # Graficar predicciones
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
        plt.savefig('prediccion_ventas.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def generar_reporte_avanzado(self):
        """Generar reporte completo de análisis avanzado"""
        print("\n" + "="*60)
        print("🚀 GENERANDO REPORTE AVANZADO DE ANÁLISIS")
        print("="*60)
        
        self.analizar_tendencias()
        self.analizar_estacionalidad()
        self.analizar_correlaciones()
        self.analizar_outliers()
        self.prediccion_simple()
        
        print("\n✅ Reporte avanzado generado exitosamente!")
        print("📁 Todas las gráficas se han guardado como archivos PNG.")

def main():
    """Función principal"""
    print("🎯 ANÁLISIS AVANZADO DE VENTAS")
    print("="*50)
    
    analizador = AnalizadorAvanzado('datos_ventas.csv')
    analizador.generar_reporte_avanzado()

if __name__ == "__main__":
    main() 