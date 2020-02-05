from __future__ import annotations
from .loader import DataLoader
from logic.observer import IObserver
from logic.notification import NotificationObservableObserver, ConsoleNotificationObserver, LoadDataEvent
from typing import List
from copy import deepcopy


class Session(object):
    __loader: DataLoader = None
    __godName: str = None
    __token: str = None
    __lastLoadDataEvent: LoadDataEvent = None
    # TODO - надо сохранять последнюю загруженную информацию для отображения

    def __init__(self):
        pass

    def get() -> Session:
        return Session()

    # Реализация одиночки
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Session, cls).__new__(cls)
        return cls.instance

    def authenticate(self, godName: str, token: str = None) -> None:
        self.__godName = godName
        self.__token = token

    def setLastLoadData(self, loadDataEvent: LoadDataEvent) -> None:
        self.__lastLoadDataEvent = loadDataEvent
    
    def getLastLoadData(self) -> LoadDataEvent:
        if (self.__lastLoadDataEvent is not None):
            return deepcopy(self.__lastLoadDataEvent)
        else:
            return None

    def isLoadPrivateInfo(self) -> bool:
        return self.__token not in (None, '')

    def startLoadData(self, observers: IObserver) -> None:
        if (self.__loader is None):
            self.__loader = DataLoader(self.__godName, self.__token)

            notificationObsarvableObserver = NotificationObservableObserver()
            notificationObsarvableObserver.register(ConsoleNotificationObserver())
            for observer in observers:
                notificationObsarvableObserver.register(observer)
            self.__loader.register(notificationObsarvableObserver)

            self.__loader.start()
        else:
            raise Exception('Загрузка данных уже работает')

    def stopLoadData(self) -> None:
        if (self.__loader is not None):
            self.__loader.stop()
            self.__loader = None

    def quit(self) -> None:
        self.stopLoadData()
