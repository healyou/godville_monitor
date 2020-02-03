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


# Событие загрузки данных
class AbstractLoaderEvent(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass


# Событие ошибки загрузки данных
class LoadErrorEvent(AbstractLoaderEvent):
    error: Exception = None
    loadDate: datetime = None

    def __init__(self, error: Exception, loadDate: datetime):
        super(AbstractLoaderEvent, self).__init__()
        self.error = error
        self.loadDate = loadDate


# Событие загрузки данных
class LoadDataEvent(AbstractLoaderEvent):
    info: IInfo = None
    loadDate: datetime = None

    def __init__(self, info: IInfo, loadDate: datetime):
        super(AbstractLoaderEvent, self).__init__()
        self.info = info
        self.loadDate = loadDate
