from abc import abstractmethod
from threading import Thread, Event, Timer
from datetime import datetime
from service.service import GodvilleApiService
from entity.entity import PrivateApiInfo, OpenApiInfo, IInfo
from .observer import IEvent, IObserver, IObservable, LoadErrorEvent, LoadDataEvent


# Поток, запускающий выполнение функции через каждый n секунд после очередного запуска
# Возможно завершение работы потока - завершит работу после последней операции
class StoppedThread(object):
    def __init__(self, rerun_seconds: int = 60):
        self.__stop = Event() 
        self._rerun_seconds = rerun_seconds
        self.__timer: Timer = None

    def stop(self):
        if (self.__timer is not None):
            self.__timer.cancel()
            self.__stop.set()
  
    # see isAlive для проверки выполнения работы потока
    def isStopped(self) -> bool: 
        return self.__stop.isSet()

    def start(self):
        # Первый раз сразу отрабатываем и запускаем таймер
        self.stoppedRun()
        self.__runTimer()

    def __runTimer(self):
        # таймер отрабатает через n секунд и вызывает функцию, которая снова запустит таймер
        if (not self.isStopped()):
            # Через n секунду начнёт выполнять снова
            self.__timer = Timer(self._rerun_seconds, self.__run)
            self.__timer.start()

    def __run(self):
        # Выполняет функцию и перезапускает таймер
        self.__runTimer()
        self.stoppedRun()

    def stop(self):
        if (self.__timer is not None):
            self.__timer.cancel()
            self.__stop.clear()

    @abstractmethod
    def stoppedRun():
        pass


# Загрузка данных годвиля
class DataLoader(StoppedThread, IObservable):
    RERUN_SECONDS = 15

    def __init__(self, godname: str = None, token: str = None):
        StoppedThread.__init__(self, self.RERUN_SECONDS)
        IObservable.__init__(self)
        self.__service = GodvilleApiService()
        self.__godname = godname
        self.__token = token

    def stoppedRun(self):
        try:
            info: IInfo = None
            if (self.__isLoadPrivateInfo()):
                info = self.__service.loadPrivateInfo(self.__godname, self.__token)
            else:
                info = self.__service.loadOpenInfo(self.__godname)

            loadDataEvent: LoadDataEvent = LoadDataEvent(info, datetime.now())
            self.notifyObservers(loadDataEvent)

        except Exception as error:
            loadErrorEvent: LoadErrorEvent = LoadErrorEvent(error, datetime.now())
            self.notifyObservers(loadErrorEvent)

    def __isLoadPrivateInfo(self) -> bool:
        return self.__token not in (None, '')

