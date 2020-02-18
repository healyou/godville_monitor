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


class Session(object):
    __loader: DataLoader = None
    __godName: str = None
    __token: str = None
    __lastLoadDataEvent: LoadDataEvent = None
    __notificationToaster: NotificationToaster = None
    __userSettings: List[ISetting] = []
    mainThread = None
    systray: SysTrayIcon = None
    __uiNotifObserver: UiNotificationObserver = None

    def __init__(self):
        pass

    def get() -> Session:
        return Session()

    def runMainThread(self):
        from ui.mainthread import ApplicationThread
        self.mainThread = ApplicationThread()
        self.mainThread.runCredential()
        self.mainThread.run()

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
        self.mainThread.closeTkinter()

    def openInfo(self) -> None:
        self.mainThread.runInfo()

    def quitAppFromSysTray(self) -> None:
        self.stopLoadData()
        self.mainThread.runCredential()

    def quit(self) -> None:
        self.stopLoadData()
        self.mainThread.quit()

    def __startNotificationToaster(self) -> None:
        self.__notificationToaster = NotificationToaster()
        self.__notificationToaster.start()
