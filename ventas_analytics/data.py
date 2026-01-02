"""
Módulo para carga y validación de datos de ventas.
"""

import logging
from pathlib import Path
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)


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
    
    def _preprocesar_datos_avanzado(self, datos: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocesar datos con campos adicionales para análisis avanzado.
        
        Args:
            datos: DataFrame con datos preprocesados básicos.
            
        Returns:
            DataFrame con campos adicionales.
        """
        datos = datos.copy()
        
        # Agregar campos temporales
        datos['dia_semana'] = datos['fecha'].dt.day_name()
        datos['mes'] = datos['fecha'].dt.month
        
        return datos
    
    @property
    def datos(self) -> pd.DataFrame:
        """Obtener los datos cargados."""
        if self._datos is None:
            raise ValueError("Los datos no han sido cargados. Llama a cargar() primero.")
        return self._datos

