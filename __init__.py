"""
阿-凡达 · 凡人AI
版本: 1.0.0

一个基于中道思想、有原则、懂时宜、会成长的凡人AI框架。
"""

from afanda.core import (
    PrincipleEngine,
    HeatEngine,
    EmotionEngine,
    EtiquetteEngine,
    GrowthEngine
)
from afanda.data import DataManager
from afanda.main import AFanDa

__version__ = "1.0.0"
__author__ = "Afanda Team"
__all__ = [
    'AFanDa',
    'PrincipleEngine',
    'HeatEngine',
    'EmotionEngine',
    'EtiquetteEngine',
    'GrowthEngine',
    'DataManager',
]