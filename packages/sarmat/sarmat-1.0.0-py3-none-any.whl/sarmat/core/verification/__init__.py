"""
Sarmat.

Ядро пакета.

Классы для проведения верификации данных.
"""
__all__ = ("VerifyOnEmptyValues", "CustomizedVerification")

from .base_verifications import VerifyOnEmptyValues
from .customize_verifications import CustomizedVerification
