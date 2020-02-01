from abc import ABCMeta, abstractmethod
from typing import List
from entity.entity import IInfo
from datetime import datetime


class IEvent(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass


# Интерфейс наблюдателя
class IObserver(metaclass=ABCMeta):
    @abstractmethod
    def update(self, event: IEvent) -> None:
        pass


# Интерфейс наблюдаемого
class IObservable(metaclass=ABCMeta):
    def __init__(self) -> None:
        self._observers: List[IObserver] = []

    def register(self, observer: IObserver) -> None:
        self._observers.append(observer)

    def notifyObservers(self, event: IEvent) -> None:
        if (event is not None):
            for observer in self._observers:
                observer.update(event)


# Событие ошибки загрузки данных
class LoadErrorEvent(IEvent):
    error: Exception = None

    def __init__(self, error: Exception):
        super(IEvent, self).__init__()
        self.error = error


# Событие загрузки данных
class LoadDataEvent(IEvent):
    info: IInfo = None
    loadDate: datetime = None

    def __init__(self, info: IInfo, loadDate: datetime):
        super(IEvent, self).__init__()
        self.info = info
        self.loadDate = loadDate
