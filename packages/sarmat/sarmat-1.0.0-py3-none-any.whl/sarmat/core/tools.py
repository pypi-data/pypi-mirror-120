# from abc import ABC, abstractmethod
#
# from .exceptions import SarmatError
#
#
# class ComparingObjectsTool(ABC):
#     """Инструмент для сравнения объектов"""
#
#     def _check_type(self, other):
#         """Проверка на соответствие типов. Объекты разных типов сравнивать нельзя"""
#         if not isinstance(other, self.__class__):
#             raise SarmatError(alt_message=f"Объекты {other.__class__} и {self.__class__} не сравнимы")
#
#     @abstractmethod
#     def __eq__(self, other):
#         """Сравнение на равенство"""
#         self._check_type(other)
#
#     @abstractmethod
#     def __ne__(self, other):
#         """Определение неравенства"""
#         self._check_type(other)
#
#     @abstractmethod
#     def __lt__(self, other):
#         """Проверка на <"""
#         self._check_type(other)
#
#     @abstractmethod
#     def __gt__(self, other):
#         """Проверка на >"""
#         self._check_type(other)
#
#     @abstractmethod
#     def __le__(self, other):
#         """Проверка на <="""
#         self._check_type(other)
#
#     @abstractmethod
#     def __ge__(self, other):
#         """Проверка на >="""
#         self._check_type(other)
#
#
# class ManagingObjectsTool(ABC):
#     """Инструмент для взаимодействия с объектом"""
#
#     def __init__(self):
#         super().__init__()
#         self._is_bound = False
#
#     @abstractmethod
#     def _find_object(self, **search_arguments) -> bool:
#         """
#         Поиск объекта в хранилище
#         Args:
#             **search_arguments:
#
#         Returns: признак удачного поиска
#
#         """
#
#     @abstractmethod
#     def create(self):
#         """Создание объекта в хранилище"""
#         self._is_bound = True
#
#     @abstractmethod
#     def edit(self):
#         """Изменение объекта в хранилище"""
#
#     @abstractmethod
#     def delete(self):
#         """Удаление объекта из хранилища"""
#         self._is_bound = False
#
#     @abstractmethod
#     def get_item(self, **search_arguments):
#         """
#         Получение объекта из хранилища
#         Args:
#             **search_arguments: параметры поиска
#         """
#         self._is_bound = self._find_object(**search_arguments)
#
#     @abstractmethod
#     def get_list(self, **search_arguments):
#         """
#         Получение списка объектов из хранилища
#         Args:
#             **search_arguments: параметры поиска
#
#         """
#
#
# class SerializingObjectTool(ABC):
#     """Сериализация / десериализация объектов"""
#
#     @abstractmethod
#     def serialize(self):
#         """Сериализация объекта"""
#
#     @abstractmethod
#     def deserialize(self):
#         """Десериализация объекта"""
#
#
# class CustomAttributesTool:
#     """Работа с дополнительными атрибутами объекта"""
