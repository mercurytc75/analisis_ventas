"""
Módulo de análisis de ventas profesional y escalable.

Este módulo proporciona funcionalidades para analizar datos de ventas,
generar estadísticas y crear visualizaciones de alta calidad.
"""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import warnings

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Suprimir warnings de matplotlib sobre estilos
warnings.filterwarnings('ignore', category=UserWarning)


@dataclass
class ConfiguracionVisualizacion:
    """Configuración centralizada para visualizaciones."""
    figsize_standard: Tuple[int, int] = (10, 6)
    figsize_wide: Tuple[int, int] = (12, 6)
    dpi: int = 300
    estilo_plt: str = 'seaborn-v0_8'
    paleta_colores: List[str] = None
    directorio_salida: str = "."
    
    def __post_init__(self):
        """Inicializar valores por defecto después de la creación."""
        if self.paleta_colores is None:
            self.paleta_colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']
        
        # Configurar estilo de matplotlib
        try:
            plt.style.use(self.estilo_plt)
        except OSError:
            logger.warning(f"Estilo {self.estilo_plt} no disponible, usando estilo por defecto")
            plt.style.use('default')
        
        sns.set_palette("husl")


class DataLoader:
    """Clase responsable de cargar y validar datos."""
    
    COLUMNAS_REQUERIDAS = ['fecha', 'producto', 'categoria', 'ventas', 'cantidad', 'region']
    
    def __init__(self, ruta_archivo: str):
        """
        Inicializar el cargador de datos.
        
        Args:
            ruta_archivo: Ruta al archivo CSV con los datos de ventas.
        """
        self.ruta_archivo = Path(ruta_archivo)
        self._datos: Optional[pd.DataFrame] = None
    
    def cargar(self) -> pd.DataFrame:
        """
        Cargar y validar datos desde el archivo CSV.
        
        Returns:
            DataFrame con los datos cargados y validados.
            
        Raises:
            FileNotFoundError: Si el archivo no existe.
            ValueError: Si los datos no tienen el formato correcto.
            pd.errors.EmptyDataError: Si el archivo está vacío.
        """
        if not self.ruta_archivo.exists():
            raise FileNotFoundError(f"El archivo {self.ruta_archivo} no existe.")
        
        logger.info(f"Cargando datos desde {self.ruta_archivo}")
        
        try:
            datos = pd.read_csv(self.ruta_archivo)
        except pd.errors.EmptyDataError:
            logger.error("El archivo CSV está vacío")
            raise
        except Exception as e:
            logger.error(f"Error al leer el archivo CSV: {e}")
            raise
        
        self._validar_datos(datos)
        datos = self._preprocesar_datos(datos)
        
        self._datos = datos
        logger.info(f"Datos cargados exitosamente: {len(datos)} registros")
        return datos
    
    def _validar_datos(self, datos: pd.DataFrame) -> None:
        """
        Validar que los datos tienen el formato correcto.
        
        Args:
            datos: DataFrame a validar.
            
        Raises:
            ValueError: Si faltan columnas requeridas o hay datos inválidos.
        """
        # Validar columnas requeridas
        columnas_faltantes = set(self.COLUMNAS_REQUERIDAS) - set(datos.columns)
        if columnas_faltantes:
            raise ValueError(
                f"Faltan las siguientes columnas requeridas: {', '.join(columnas_faltantes)}"
            )
        
        # Validar que no esté vacío
        if datos.empty:
            raise ValueError("El DataFrame está vacío")
        
        # Validar tipos de datos
        if not pd.api.types.is_numeric_dtype(datos['ventas']):
            raise ValueError("La columna 'ventas' debe ser numérica")
        
        if not pd.api.types.is_numeric_dtype(datos['cantidad']):
            raise ValueError("La columna 'cantidad' debe ser numérica")
        
        # Validar valores negativos
        if (datos['ventas'] < 0).any():
            logger.warning("Se encontraron ventas negativas en los datos")
        
        if (datos['cantidad'] < 0).any():
            logger.warning("Se encontraron cantidades negativas en los datos")
    
    def _preprocesar_datos(self, datos: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocesar y limpiar los datos.
        
        Args:
            datos: DataFrame con datos sin procesar.
            
        Returns:
            DataFrame preprocesado.
        """
        datos = datos.copy()
        
        # Convertir fecha a datetime
        datos['fecha'] = pd.to_datetime(datos['fecha'], errors='coerce')
        
        # Verificar fechas inválidas
        fechas_invalidas = datos['fecha'].isna().sum()
        if fechas_invalidas > 0:
            logger.warning(f"Se encontraron {fechas_invalidas} fechas inválidas")
        
        # Eliminar filas con valores críticos faltantes
        datos = datos.dropna(subset=['ventas', 'cantidad', 'fecha'])
        
        return datos
    
    @property
    def datos(self) -> pd.DataFrame:
        """Obtener los datos cargados."""
        if self._datos is None:
            raise ValueError("Los datos no han sido cargados. Llama a cargar() primero.")
        return self._datos


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
        orientacion_horizontal: bool = False
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
        nombre_archivo: str
    ) -> None:
        """
        Crear gráfica de torta (pie chart).
        
        Args:
            datos: Series con los datos a graficar.
            titulo: Título de la gráfica.
            nombre_archivo: Nombre del archivo para guardar.
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
        plt.close()
    
    def graficar_linea_temporal(
        self,
        datos: pd.DataFrame,
        columna_fecha: str,
        columna_valor: str,
        titulo: str,
        etiqueta_x: str,
        etiqueta_y: str,
        nombre_archivo: str
    ) -> None:
        """
        Crear gráfica de línea temporal.
        
        Args:
            datos: DataFrame con datos temporales.
            columna_fecha: Nombre de la columna con fechas.
            columna_valor: Nombre de la columna con valores.
            titulo: Título de la gráfica.
            etiqueta_x: Etiqueta del eje X.
            etiqueta_y: Etiqueta del eje Y.
            nombre_archivo: Nombre del archivo para guardar.
        """
        fig, ax = plt.subplots(figsize=self.config.figsize_wide)
        
        ax.plot(
            datos[columna_fecha],
            datos[columna_valor],
            marker='o',
            linewidth=2,
            markersize=6,
            color=self.config.paleta_colores[2]
        )
        ax.set_title(titulo, fontsize=16, fontweight='bold')
        ax.set_xlabel(etiqueta_x, fontsize=12)
        ax.set_ylabel(etiqueta_y, fontsize=12)
        ax.grid(True, alpha=0.3)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        ruta_completa = self.directorio_salida / nombre_archivo
        plt.savefig(ruta_completa, dpi=self.config.dpi, bbox_inches='tight')
        logger.info(f"Gráfica guardada: {ruta_completa}")
        plt.close()


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


class AnalizadorVentas:
    """
    Clase principal para análisis de ventas.
    
    Esta clase orquesta todas las operaciones de análisis, estadísticas
    y visualizaciones siguiendo el principio de responsabilidad única.
    """
    
    def __init__(
        self,
        archivo_datos: str,
        config_visualizacion: Optional[ConfiguracionVisualizacion] = None
    ):
        """
        Inicializar el analizador de ventas.
        
        Args:
            archivo_datos: Ruta al archivo CSV con datos de ventas.
            config_visualizacion: Configuración para visualizaciones. Si es None, usa valores por defecto.
        """
        self.loader = DataLoader(archivo_datos)
        self.config = config_visualizacion or ConfiguracionVisualizacion()
        self.visualizador = VisualizadorVentas(self.config)
        self._datos: Optional[pd.DataFrame] = None
        self._estadisticas: Optional[EstadisticasVentas] = None
    
    def cargar_datos(self) -> None:
        """Cargar datos desde el archivo."""
        self._datos = self.loader.cargar()
        self._estadisticas = EstadisticasVentas(self._datos)
    
    @property
    def datos(self) -> pd.DataFrame:
        """Obtener los datos cargados."""
        if self._datos is None:
            self.cargar_datos()
        return self._datos
    
    @property
    def estadisticas(self) -> EstadisticasVentas:
        """Obtener el calculador de estadísticas."""
        if self._estadisticas is None:
            self.cargar_datos()
        return self._estadisticas
    
    def mostrar_resumen_estadistico(self) -> None:
        """Mostrar resumen estadístico en consola."""
        PresentadorReporte.mostrar_resumen_estadistico(self.estadisticas)
    
    def graficar_ventas_por_categoria(self) -> None:
        """Crear gráfica de ventas por categoría."""
        datos = self.estadisticas.obtener_ventas_por_categoria()
        self.visualizador.graficar_barras(
            datos=datos,
            titulo='Ventas Totales por Categoría',
            etiqueta_x='Categoría',
            etiqueta_y='Ventas ($)',
            nombre_archivo='ventas_por_categoria.png'
        )
    
    def graficar_ventas_por_region(self) -> None:
        """Crear gráfica de ventas por región."""
        datos = self.estadisticas.obtener_ventas_por_region()
        self.visualizador.graficar_torta(
            datos=datos,
            titulo='Distribución de Ventas por Región',
            nombre_archivo='ventas_por_region.png'
        )
    
    def graficar_evolucion_ventas(self) -> None:
        """Crear gráfica de evolución de ventas en el tiempo."""
        datos = self.estadisticas.obtener_evolucion_temporal()
        self.visualizador.graficar_linea_temporal(
            datos=datos,
            columna_fecha='fecha',
            columna_valor='ventas',
            titulo='Evolución de Ventas Diarias',
            etiqueta_x='Fecha',
            etiqueta_y='Ventas ($)',
            nombre_archivo='evolucion_ventas.png'
        )
    
    def graficar_productos_mas_vendidos(self) -> None:
        """Crear gráfica de productos más vendidos."""
        datos = self.estadisticas.obtener_productos_mas_vendidos()
        self.visualizador.graficar_barras(
            datos=datos,
            titulo='Productos Más Vendidos (por cantidad)',
            etiqueta_x='Cantidad Vendida',
            etiqueta_y='Producto',
            nombre_archivo='productos_mas_vendidos.png',
            orientacion_horizontal=True
        )
    
    def generar_reporte_completo(self, mostrar_graficas: bool = False) -> None:
        """
        Generar un reporte completo con todas las visualizaciones.
        
        Args:
            mostrar_graficas: Si es True, muestra las gráficas además de guardarlas.
        """
        logger.info("Iniciando generación de reporte completo")
        
        print("\n" + "=" * 60)
        print("🚀 GENERANDO REPORTE COMPLETO DE ANÁLISIS DE VENTAS")
        print("=" * 60)
        
        # Mostrar resumen estadístico
        self.mostrar_resumen_estadistico()
        
        # Generar todas las gráficas
        print("\n📊 Generando visualizaciones...")
        try:
            self.graficar_ventas_por_categoria()
            self.graficar_ventas_por_region()
            self.graficar_evolucion_ventas()
            self.graficar_productos_mas_vendidos()
            
            print("\n✅ Reporte completo generado exitosamente!")
            print(f"📁 Las gráficas se han guardado en: {Path(self.config.directorio_salida).absolute()}")
        except Exception as e:
            logger.error(f"Error al generar visualizaciones: {e}", exc_info=True)
            raise


def main() -> None:
    """Función principal del programa."""
    print("🎯 ANÁLISIS DE VENTAS - HERRAMIENTA DE ANÁLISIS")
    print("=" * 50)
    
    try:
        # Crear instancia del analizador
        analizador = AnalizadorVentas('datos_ventas.csv')
        
        # Generar reporte completo
        analizador.generar_reporte_completo()
    except FileNotFoundError as e:
        logger.error(f"Error: {e}")
        print(f"❌ Error: {e}")
    except ValueError as e:
        logger.error(f"Error de validación: {e}")
        print(f"❌ Error de validación: {e}")
    except Exception as e:
        logger.error(f"Error inesperado: {e}", exc_info=True)
        print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()
