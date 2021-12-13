from abc import ABCMeta, abstractmethod,abstractproperty



class Scenario:
    __metaclass__=ABCMeta

    @abstractmethod
    def generate_scenario(self):
        """Генератор сценария"""

    @abstractmethod
    def  get_next_transitions(self):
        """Получить дальнейшие переходы"""
    @abstractmethod
    def get_next_description(self):
        """Пользовательское описание"""
