from abc import ABCMeta, abstractmethod,abstractproperty


class BotInterface:
    __metaclass__=ABCMeta

    @abstractmethod
    def start(self):
        """Запуск бота"""
    @abstractmethod
    def stop(self):
        """Остановка бота"""
