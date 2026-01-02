"""
Módulo para generación de visualizaciones de ventas.
"""

from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd

from ventas_analytics.config import ConfiguracionVisualizacion

import logging
logger = logging.getLogger(__name__)


class VisualizadorVentas:
    """Clase responsable de generar visualizaciones de ventas."""
    
    def __init__(self, config: Optional[ConfiguracionVisualizacion] = None):
        """
        Inicializar el visualizador.
        
        Args:
            config: Configuración para visualizaciones. Si es None, usa configuración por defecto.
        """
        self.config = config or ConfiguracionVisualizacion()
        self.directorio_salida = Path(self.config.directorio_salida)
        self.directorio_salida.mkdir(parents=True, exist_ok=True)
    
    def graficar_barras(
        self,
        datos: pd.Series,
        titulo: str,
        etiqueta_x: str,
        etiqueta_y: str,
        nombre_archivo: str,
        orientacion_horizontal: bool = False,
        mostrar: bool = False
    ) -> None:
        """
        Crear gráfica de barras.
        
        Args:
            datos: Series con los datos a graficar.
            titulo: Título de la gráfica.
            etiqueta_x: Etiqueta del eje X.
            etiqueta_y: Etiqueta del eje Y.
            nombre_archivo: Nombre del archivo para guardar.
            orientacion_horizontal: Si es True, crea barras horizontales.
            mostrar: Si es True, muestra la gráfica además de guardarla.
        """
        fig, ax = plt.subplots(figsize=self.config.figsize_standard)
        
        if orientacion_horizontal:
            bars = ax.barh(datos.index, datos.values, color=self.config.paleta_colores[0])
            self._agregar_valores_barras_horizontales(ax, bars)
        else:
            bars = ax.bar(datos.index, datos.values, color=self.config.paleta_colores[0], edgecolor='navy')
            self._agregar_valores_barras_verticales(ax, bars)
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        ax.set_title(titulo, fontsize=16, fontweight='bold')
        ax.set_xlabel(etiqueta_x, fontsize=12)
        ax.set_ylabel(etiqueta_y, fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        ruta_completa = self.directorio_salida / nombre_archivo
        plt.savefig(ruta_completa, dpi=self.config.dpi, bbox_inches='tight')
        logger.info(f"Gráfica guardada: {ruta_completa}")
        
        if mostrar:
            plt.show()
        else:
            plt.close()
    
    def _agregar_valores_barras_verticales(self, ax: plt.Axes, bars) -> None:
        """Agregar valores numéricos sobre las barras verticales."""
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.,
                height + height * 0.01,
                f'${height:,.0f}',
                ha='center',
                va='bottom',
                fontweight='bold'
            )
    
    def _agregar_valores_barras_horizontales(self, ax: plt.Axes, bars) -> None:
        """Agregar valores numéricos en las barras horizontales."""
        for bar in bars:
            width = bar.get_width()
            ax.text(
                width + 0.1,
                bar.get_y() + bar.get_height() / 2,
                str(int(width)),
                ha='left',
                va='center',
                fontweight='bold'
            )
    
    def graficar_torta(
        self,
        datos: pd.Series,
        titulo: str,
        nombre_archivo: str,
        mostrar: bool = False
    ) -> None:
        """
        Crear gráfica de torta (pie chart).
        
        Args:
            datos: Series con los datos a graficar.
            titulo: Título de la gráfica.
            nombre_archivo: Nombre del archivo para guardar.
            mostrar: Si es True, muestra la gráfica además de guardarla.
        """
        fig, ax = plt.subplots(figsize=self.config.figsize_standard)
        
        colores = self.config.paleta_colores[:len(datos)]
        explode = [0.05] * len(datos)
        
        ax.pie(
            datos.values,
            labels=datos.index,
            autopct='%1.1f%%',
            colors=colores,
            startangle=90,
            explode=explode
        )
        ax.set_title(titulo, fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        ruta_completa = self.directorio_salida / nombre_archivo
        plt.savefig(ruta_completa, dpi=self.config.dpi, bbox_inches='tight')
        logger.info(f"Gráfica guardada: {ruta_completa}")
        
        if mostrar:
            plt.show()
        else:
            plt.close()
    
    def graficar_linea_temporal(
        self,
        datos: pd.DataFrame,
        columna_fecha: str,
        columna_valor: str,
        titulo: str,
        etiqueta_x: str,
        etiqueta_y: str,
        nombre_archivo: str,
        mostrar: bool = False,
        etiquetas_lineas: Optional[list] = None
    ) -> None:
        """
        Crear gráfica de línea temporal.
        
        Args:
            datos: DataFrame con datos temporales.
            columna_fecha: Nombre de la columna con fechas.
            columna_valor: Nombre de la columna con valores (o lista de columnas).
            titulo: Título de la gráfica.
            etiqueta_x: Etiqueta del eje X.
            etiqueta_y: Etiqueta del eje Y.
            nombre_archivo: Nombre del archivo para guardar.
            mostrar: Si es True, muestra la gráfica además de guardarla.
            etiquetas_lineas: Lista de etiquetas para múltiples líneas.
        """
        fig, ax = plt.subplots(figsize=self.config.figsize_wide)
        
        if isinstance(columna_valor, str):
            ax.plot(
                datos[columna_fecha],
                datos[columna_valor],
                marker='o',
                linewidth=2,
                markersize=6,
                color=self.config.paleta_colores[2]
            )
        else:
            # Múltiples líneas
            for i, col in enumerate(columna_valor):
                label = etiquetas_lineas[i] if etiquetas_lineas else col
                ax.plot(
                    datos[columna_fecha],
                    datos[col],
                    marker='o',
                    linewidth=2,
                    markersize=6,
                    label=label,
                    color=self.config.paleta_colores[i % len(self.config.paleta_colores)]
                )
            ax.legend()
        
        ax.set_title(titulo, fontsize=16, fontweight='bold')
        ax.set_xlabel(etiqueta_x, fontsize=12)
        ax.set_ylabel(etiqueta_y, fontsize=12)
        ax.grid(True, alpha=0.3)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        ruta_completa = self.directorio_salida / nombre_archivo
        plt.savefig(ruta_completa, dpi=self.config.dpi, bbox_inches='tight')
        logger.info(f"Gráfica guardada: {ruta_completa}")
        
        if mostrar:
            plt.show()
        else:
            plt.close()
    
    def graficar_boxplot(
        self,
        datos: pd.Series,
        titulo: str,
        etiqueta_y: str,
        nombre_archivo: str,
        mostrar: bool = False
    ) -> None:
        """
        Crear gráfica de boxplot.
        
        Args:
            datos: Series con los datos a graficar.
            titulo: Título de la gráfica.
            etiqueta_y: Etiqueta del eje Y.
            nombre_archivo: Nombre del archivo para guardar.
            mostrar: Si es True, muestra la gráfica además de guardarla.
        """
        fig, ax = plt.subplots(figsize=self.config.figsize_standard)
        
        ax.boxplot(datos, patch_artist=True, boxprops=dict(facecolor='lightblue'))
        ax.set_title(titulo, fontsize=16, fontweight='bold')
        ax.set_ylabel(etiqueta_y, fontsize=12)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        ruta_completa = self.directorio_salida / nombre_archivo
        plt.savefig(ruta_completa, dpi=self.config.dpi, bbox_inches='tight')
        logger.info(f"Gráfica guardada: {ruta_completa}")
        
        if mostrar:
            plt.show()
        else:
            plt.close()
    
    def graficar_heatmap(
        self,
        datos: pd.DataFrame,
        titulo: str,
        nombre_archivo: str,
        mostrar: bool = False
    ) -> None:
        """
        Crear mapa de calor (heatmap).
        
        Args:
            datos: DataFrame con datos de correlación.
            titulo: Título de la gráfica.
            nombre_archivo: Nombre del archivo para guardar.
            mostrar: Si es True, muestra la gráfica además de guardarla.
        """
        import seaborn as sns
        
        fig, ax = plt.subplots(figsize=self.config.figsize_standard)
        
        sns.heatmap(
            datos,
            annot=True,
            cmap='coolwarm',
            center=0,
            square=True,
            linewidths=0.5,
            ax=ax
        )
        ax.set_title(titulo, fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        ruta_completa = self.directorio_salida / nombre_archivo
        plt.savefig(ruta_completa, dpi=self.config.dpi, bbox_inches='tight')
        logger.info(f"Gráfica guardada: {ruta_completa}")
        
        if mostrar:
            plt.show()
        else:
            plt.close()

