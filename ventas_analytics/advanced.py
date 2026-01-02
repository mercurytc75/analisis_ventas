"""
Módulo para análisis avanzado de ventas (tendencias, correlaciones, predicciones).
"""

from datetime import timedelta
from typing import Dict, Tuple, Optional

import numpy as np
import pandas as pd
from scipy import stats

from ventas_analytics.data import DataLoader
from ventas_analytics.statistics import EstadisticasVentas
from ventas_analytics.visualization import VisualizadorVentas
from ventas_analytics.config import ConfiguracionVisualizacion

import logging
logger = logging.getLogger(__name__)


class AnalizadorAvanzado:
    """Clase para análisis estadístico avanzado de ventas."""
    
    def __init__(
        self,
        datos: pd.DataFrame,
        config: Optional[ConfiguracionVisualizacion] = None
    ):
        """
        Inicializar el analizador avanzado.
        
        Args:
            datos: DataFrame con datos de ventas.
            config: Configuración para visualizaciones.
        """
        self.datos = datos.copy()
        self._preparar_datos_avanzados()
        self.estadisticas = EstadisticasVentas(self.datos)
        self.visualizador = VisualizadorVentas(config)
        self.config = config or ConfiguracionVisualizacion()
    
    def _preparar_datos_avanzados(self) -> None:
        """Preparar datos con campos adicionales para análisis avanzado."""
        if 'dia_semana' not in self.datos.columns:
            self.datos['dia_semana'] = self.datos['fecha'].dt.day_name()
        if 'mes' not in self.datos.columns:
            self.datos['mes'] = self.datos['fecha'].dt.month
    
    def analizar_tendencias(self) -> Dict[str, float]:
        """
        Analizar tendencias en las ventas usando regresión lineal.
        
        Returns:
            Diccionario con métricas de tendencia.
        """
        ventas_diarias = self.estadisticas.obtener_evolucion_temporal()
        
        x = np.arange(len(ventas_diarias))
        y = ventas_diarias['ventas'].values
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        resultado = {
            'pendiente': float(slope),
            'intercepto': float(intercept),
            'r_cuadrado': float(r_value ** 2),
            'valor_p': float(p_value),
            'error_estandar': float(std_err)
        }
        
        return resultado
    
    def obtener_ventas_por_dia_semana(self) -> pd.Series:
        """
        Obtener ventas agrupadas por día de la semana.
        
        Returns:
            Series con ventas por día de la semana.
        """
        orden_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        ventas_dia = self.datos.groupby('dia_semana')['ventas'].sum()
        return ventas_dia.reindex([d for d in orden_dias if d in ventas_dia.index])
    
    def analizar_correlaciones(self) -> pd.DataFrame:
        """
        Analizar correlaciones entre variables numéricas.
        
        Returns:
            DataFrame con matriz de correlaciones.
        """
        datos_corr = self.datos.copy()
        datos_corr['categoria_num'] = pd.Categorical(datos_corr['categoria']).codes
        datos_corr['region_num'] = pd.Categorical(datos_corr['region']).codes
        
        correlaciones = datos_corr[['ventas', 'cantidad', 'categoria_num', 'region_num']].corr()
        return correlaciones
    
    def detectar_outliers(self, columna: str = 'ventas') -> Tuple[pd.DataFrame, Dict[str, float]]:
        """
        Detectar outliers usando el método IQR.
        
        Args:
            columna: Nombre de la columna a analizar.
            
        Returns:
            Tupla con (DataFrame de outliers, diccionario con límites).
        """
        Q1 = self.datos[columna].quantile(0.25)
        Q3 = self.datos[columna].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = self.datos[
            (self.datos[columna] < lower_bound) | 
            (self.datos[columna] > upper_bound)
        ]
        
        limites = {
            'Q1': float(Q1),
            'Q3': float(Q3),
            'IQR': float(IQR),
            'limite_inferior': float(lower_bound),
            'limite_superior': float(upper_bound)
        }
        
        return outliers, limites
    
    def predecir_ventas(
        self,
        dias_futuros: int = 5,
        metodo: str = 'lineal'
    ) -> pd.DataFrame:
        """
        Predecir ventas futuras usando regresión lineal.
        
        Args:
            dias_futuros: Número de días a predecir.
            metodo: Método de predicción ('lineal').
            
        Returns:
            DataFrame con fechas y predicciones.
        """
        ventas_diarias = self.estadisticas.obtener_evolucion_temporal()
        x = np.arange(len(ventas_diarias))
        y = ventas_diarias['ventas'].values
        
        slope, intercept, _, _, _ = stats.linregress(x, y)
        
        ultima_fecha = ventas_diarias['fecha'].max()
        predicciones = []
        fechas_pred = []
        
        for i in range(1, dias_futuros + 1):
            fecha_pred = ultima_fecha + timedelta(days=i)
            pred = slope * (len(ventas_diarias) + i - 1) + intercept
            predicciones.append(max(0, pred))  # No ventas negativas
            fechas_pred.append(fecha_pred)
        
        return pd.DataFrame({
            'fecha': fechas_pred,
            'prediccion': predicciones
        })
    
    def graficar_tendencia(self, nombre_archivo: str = 'tendencia_ventas.png', mostrar: bool = False) -> None:
        """Graficar ventas con línea de tendencia."""
        ventas_diarias = self.estadisticas.obtener_evolucion_temporal()
        tendencia = self.analizar_tendencias()
        
        x = np.arange(len(ventas_diarias))
        trend_line = tendencia['pendiente'] * x + tendencia['intercepto']
        
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(figsize=self.config.figsize_wide)
        ax.plot(
            ventas_diarias['fecha'],
            ventas_diarias['ventas'],
            marker='o',
            linewidth=2,
            markersize=6,
            label='Ventas reales'
        )
        ax.plot(
            ventas_diarias['fecha'],
            trend_line,
            'r--',
            linewidth=2,
            label='Tendencia'
        )
        ax.set_title('Análisis de Tendencia de Ventas', fontsize=16, fontweight='bold')
        ax.set_xlabel('Fecha', fontsize=12)
        ax.set_ylabel('Ventas ($)', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        from pathlib import Path
        plt.tight_layout()
        ruta_completa = Path(self.config.directorio_salida) / nombre_archivo
        plt.savefig(ruta_completa, dpi=self.config.dpi, bbox_inches='tight')
        logger.info(f"Gráfica guardada: {ruta_completa}")
        
        if mostrar:
            plt.show()
        else:
            plt.close()
    
    def graficar_estacionalidad_semanal(
        self,
        nombre_archivo: str = 'estacionalidad_semanal.png',
        mostrar: bool = False
    ) -> None:
        """Graficar estacionalidad semanal."""
        ventas_dia = self.obtener_ventas_por_dia_semana()
        self.visualizador.graficar_barras(
            datos=ventas_dia,
            titulo='Ventas por Día de la Semana',
            etiqueta_x='Día de la Semana',
            etiqueta_y='Ventas ($)',
            nombre_archivo=nombre_archivo,
            mostrar=mostrar
        )
    
    def graficar_correlaciones(
        self,
        nombre_archivo: str = 'correlaciones.png',
        mostrar: bool = False
    ) -> None:
        """Graficar matriz de correlaciones."""
        correlaciones = self.analizar_correlaciones()
        self.visualizador.graficar_heatmap(
            datos=correlaciones,
            titulo='Matriz de Correlaciones',
            nombre_archivo=nombre_archivo,
            mostrar=mostrar
        )
    
    def graficar_outliers(
        self,
        columna: str = 'ventas',
        nombre_archivo: str = 'outliers_ventas.png',
        mostrar: bool = False
    ) -> None:
        """Graficar boxplot para detectar outliers."""
        self.visualizador.graficar_boxplot(
            datos=self.datos[columna],
            titulo='Distribución de Ventas (Boxplot)',
            etiqueta_y='Ventas ($)',
            nombre_archivo=nombre_archivo,
            mostrar=mostrar
        )
    
    def graficar_predicciones(
        self,
        dias_futuros: int = 5,
        nombre_archivo: str = 'prediccion_ventas.png',
        mostrar: bool = False
    ) -> None:
        """Graficar predicciones de ventas."""
        ventas_diarias = self.estadisticas.obtener_evolucion_temporal()
        predicciones = self.predecir_ventas(dias_futuros)
        
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(figsize=self.config.figsize_wide)
        ax.plot(
            ventas_diarias['fecha'],
            ventas_diarias['ventas'],
            marker='o',
            linewidth=2,
            markersize=6,
            label='Ventas reales'
        )
        ax.plot(
            predicciones['fecha'],
            predicciones['prediccion'],
            'r--',
            marker='s',
            linewidth=2,
            markersize=6,
            label='Predicciones'
        )
        ax.set_title(f'Predicción de Ventas (Próximos {dias_futuros} días)', fontsize=16, fontweight='bold')
        ax.set_xlabel('Fecha', fontsize=12)
        ax.set_ylabel('Ventas ($)', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        from pathlib import Path
        plt.tight_layout()
        ruta_completa = Path(self.config.directorio_salida) / nombre_archivo
        plt.savefig(ruta_completa, dpi=self.config.dpi, bbox_inches='tight')
        logger.info(f"Gráfica guardada: {ruta_completa}")
        
        if mostrar:
            plt.show()
        else:
            plt.close()

