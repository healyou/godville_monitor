from abc import abstractmethod
from threading import Thread, Event, Timer
from datetime import datetime
from service.service import GodvilleApiService
from entity.entity import PrivateApiInfo, OpenApiInfo, IInfo
from .observer import IEvent, IObserver, IObservable, LoadErrorEvent, LoadDataEvent


# Поток, запускающий выполнение функции через каждый n секунд после очередного запуска
# Возможно завершение работы потока - завершит работу после последней операции
class StoppedThread(Thread):
    def __init__(self, rerun_seconds: int = 60):
        Thread.__init__(self)
        self.daemon: bool = True
        self.__stop = Event() 
        self._rerun_seconds = rerun_seconds

    def stop(self):
        self.__stop.set()
  
    # see isAlive для проверки выполнения работы потока
    def isStopped(self) -> bool: 
        return self.__stop.isSet()

    def run(self):
        # Первый запуск сразу
        if (not self.isStopped()):
            Thread(daemon=True, target=self.stoppedRun).run()

        # Остальные запуски, пока не завершим поток
        while not self.isStopped():
            # Через n секунду начнёт выполнять снова
            Timer(interval=self._rerun_seconds, function=self.stoppedRun).run()

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
        return self.__token is not None

