from __future__ import annotations
from .loader import DataLoader
from logic.observer import IObserver
from logic.notification import NotificationObservableObserver, ConsoleNotificationObserver
from typing import List


class Session(object):
    __loader: DataLoader = None
    __godName: str = None
    __token: str = None

    def __init__(self):
        pass

    def get() -> Session:
        return Session()

    # Реализация одиночки
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Session, cls).__new__(cls)
        return cls.instance

    def authenticate(self, godName: str, token: str = None):
        self.__godName = godName
        self.__token = token

    def startLoadData(self, observers: IObserver):
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

    def stopLoadData(self):
        if (self.__loader is not None):
            self.__loader.stop()
            # TODO - почему-то поток не вырубается и на join зависает
            # if (self.__loader.isAlive()):
            #     self.__loader.join()

    def quit(self):
        self.stopLoadData()
