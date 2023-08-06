"""
Sarmat.

Ядро пакета.

Классы для проведения верификации данных.

Классы базовой верификации.
"""
from abc import ABC, abstractmethod

from ..exceptions import ErrorCode, SarmatException


class Verification(ABC):
    """Базовый класс проверки."""

    def __init__(self, parent=None):
        self._parent = parent

    @abstractmethod
    def verify(self) -> None:
        """Объект проверяет свои атрибуты."""
        if self._parent:
            self._parent.verify()


class VerifyOnEmptyValues(Verification):
    """
    Проверка на непустоту атрибутов.

    Если атрибут отсутствует, будет вызвана ошибка.
    """

    attributes = []

    def verify(self) -> None:
        for attr in self.attributes:
            if hasattr(self, attr):
                if getattr(self, attr) is None:
                    raise SarmatException(attr, err_code=ErrorCode.NOT_FILLED)
            else:
                raise SarmatException(attr, err_code=ErrorCode.NO_ATTRIBUTE)

        super().verify()
