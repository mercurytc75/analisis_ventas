"""
Módulo de configuración para el análisis de ventas.

Define configuraciones centralizadas para visualizaciones y otros aspectos del sistema.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
import warnings

import matplotlib.pyplot as plt
import seaborn as sns
import logging

logger = logging.getLogger(__name__)
warnings.filterwarnings('ignore', category=UserWarning)


@dataclass
class ConfiguracionVisualizacion:
    """Configuración centralizada para visualizaciones."""
    figsize_standard: Tuple[int, int] = (10, 6)
    figsize_wide: Tuple[int, int] = (12, 6)
    dpi: int = 300
    estilo_plt: str = 'seaborn-v0_8'
    paleta_colores: Optional[List[str]] = None
    directorio_salida: str = "."
    
    def __post_init__(self) -> None:
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

