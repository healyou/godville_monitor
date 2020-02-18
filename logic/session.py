from __future__ import annotations
from .loader import DataLoader, NotificationToaster
from logic.observer import IObserver
from logic.notification import NotificationObservableObserver, ConsoleNotificationObserver, LoadDataEvent, UiNotificationObserver
from typing import List
from copy import deepcopy
from win10toast import ToastNotifier
from entity.settings import ISetting
from service.settings import SettingsService
from infi.systray import SysTrayIcon
from ui.mainthread import ApplicationThread


class Session(object):
    __loader: DataLoader = None
    __godName: str = None
    __token: str = None
    __lastLoadDataEvent: LoadDataEvent = None
    __notificationToaster: NotificationToaster = None
    __userSettings: List[ISetting] = []
    __mainTkinterThread: ApplicationThread = None
    __uiNotifObserver: UiNotificationObserver = None
    __systray: SysTrayIcon = None

    def __init__(self):
        pass

    def get() -> Session:
        return Session()

    # Запуск потока работы ui
    def runTkinterCredentional(self):
        from ui.mainthread import ApplicationThread
        self.__mainTkinterThread = ApplicationThread(self.quit)
        self.__mainTkinterThread.runCredential()
        self.__mainTkinterThread.run()

    # Реализация одиночки
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Session, cls).__new__(cls)
        return cls.instance

    def authenticate(self, godName: str, token: str = None) -> None:
        self.__godName = godName
        self.__token = token

        try:
            self.__userSettings = SettingsService.get().loadSettings()
        except Exception as err:
            self.__userSettings = []

    def setLastLoadData(self, loadDataEvent: LoadDataEvent) -> None:
        self.__lastLoadDataEvent = loadDataEvent

    def getLastLoadData(self) -> LoadDataEvent:
        if (self.__lastLoadDataEvent is not None):
            return deepcopy(self.__lastLoadDataEvent)
        else:
            return None

    def isLoadPrivateInfo(self) -> bool:
        return self.__token not in (None, '')

    def startLoadData(self) -> None:
        if (self.__loader is None):
            self.__loader = DataLoader(self.__godName, self.__token)
            self.__uiNotifObserver = UiNotificationObserver()

            notificationObsarvableObserver = NotificationObservableObserver()
            notificationObsarvableObserver.register(ConsoleNotificationObserver())
            notificationObsarvableObserver.register(self.__uiNotifObserver)
            self.__loader.register(notificationObsarvableObserver)

            self.__loader.start()

            self.__startNotificationToaster()

    def setUiNotificationObserver(self, observer: IObserver) -> None:
        self.__uiNotifObserver.setUiObserver(observer)

    def stopLoadData(self) -> None:
        if (self.__loader is not None):
            self.__loader.stop()
            self.__loader = None
        if (self.__notificationToaster is not None):
            self.__notificationToaster.stop()
            self.__notificationToaster = None

    def setUserSettigns(self, settings: List[ISetting]) -> Mone:
        self.__userSettings = settings
    
    def getUserSettings(self) -> List[ISetting]:
        return self.__userSettings

    def closeTkinter(self) -> None:
        self.__uiNotifObserver.clearUiObserver()
        self.__mainTkinterThread.closeTkinterAndWait()

    def openInfo(self) -> None:
        self.__mainTkinterThread.runInfo()

    # Открытие tkinter, если хотим выйти из приложения в трее
    def quitAppFromSysTray(self) -> None:
        self.stopLoadData()
        self.__mainTkinterThread.runCredential()

    # Завершение работы приложения
    def quit(self) -> None:
        self.stopLoadData()
        self.__mainTkinterThread.quitTkAndThread()

    def __startNotificationToaster(self) -> None:
        self.__notificationToaster = NotificationToaster()
        self.__notificationToaster.start()

    # Сворачивание приложения в трей (tkinter off, но поток чтения работает)
    def openSysTray(self):
        def sysTrayInfoOpenClick(systray):
            self.openInfo()
        def sysTrayQuitCallback(systray):
            self.quitAppFromSysTray()

        self.closeTkinter()
        menu_options = (('Развернуть', None, sysTrayInfoOpenClick),)
        self.__systray = SysTrayIcon("python.ico", 'Godville следилка', menu_options, on_quit=sysTrayQuitCallback)
        self.__systray.start()

    # Завершение работы трея, если он был включен
    def closeSysTray(self):
        if self.__systray:
            self.__systray.shutdown()
            self.__systray = None
