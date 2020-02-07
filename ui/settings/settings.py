from tkinter import *
from .contract import ISettingsView, ISettingsPresenter
from typing import List, Dict
from logic.notification import IEvent, NotificationEvent, LoadDataEvent, LoadErrorEvent, ChangePropertiesNotificationEvent
from logic.notification_items import NotificationItem
from ui.component.scrollableframe import VerticalScrolledFrame
from service.settings import SettingsService


class SettingsView(ISettingsView):
    __presenter: ISettingsPresenter = None
    __root: Tk = None
    __frame: Frame = None
    __settings: Dict = {}

    def __init__(self, root: Tk):
        ISettingsView.__init__(self)
        self.__presenter = SettingsPresenter(self)
        self.__root = root
        self.__initFrame()
        self.__presenter.afterInitView()

    def __initFrame(self):
        self.__clearChildrens()

        # scrolledFrame = VerticalScrolledFrame(self.__root)
        # self.__frame = scrolledFrame.interior
        # TODO добавить скролл
        self.__frame = Frame(master=self.__root, bd=1, relief=SUNKEN)
        self.__frame.pack(fill=BOTH, expand=True, padx=5, pady=5)
        #self.__frame.grid(row=0, column=0)

        self.__loadDataLabel = Label(master=self.__frame, text='Ещё не было загрузки данных')
        self.__loadDataLabel.pack(side=TOP, padx=5, pady=5)

        i: int = 1
        for notifItem in [NotificationItem.GOD_NAME, NotificationItem.HERO_NAME]:
            frame = Frame(master=self.__frame, bd=1, relief=SUNKEN)
            frame.pack(side=TOP, fill=X, expand=True)

            settingVar = BooleanVar()
            settingVar.set(False)
            settingCheckBox = Checkbutton(master=frame, text=notifItem.propertyName, variable=settingVar, onvalue=True, offvalue=False)
            settingCheckBox.pack(side=TOP, padx=5)
            self.__settings[notifItem.propertyName] = settingVar
            i += 1

        enterButton = Button(master=self.__frame, text='Назад', command=self.__onBackClick)
        enterButton.pack(side=TOP, padx=5, pady=5)

        saveButton = Button(master=self.__frame, text='Сохранить', command=self.__onSaveSetingsClick)
        saveButton.pack(side=TOP, padx=5, pady=5)

    def __onBackClick(self):
        self.__presenter.backClick()

    def __onSaveSetingsClick(self):
        self.__presenter.saveSettinsClick(self.__settings)

    def __clearChildrens(self):
        for widget in self.__root.winfo_children():
            widget.destroy()

    def showCredentionalView(self) -> None:
        from ui.credential.credentional import CredentionalView
        CredentionalView(self.__root)

    def showSettings(self) -> None:
        pass

    def showMessage(self, message: str) -> None:
        # TODO - реализовать
        pass


class SettingsPresenter(ISettingsPresenter):
    __view: ISettingsView = None

    def __init__(self, view: ISettingsView):
        ISettingsPresenter.__init__(self)
        self.__view = view

    def backClick(self) -> None:
        self.__view.showCredentionalView()

    def afterInitView(self) -> None:
        # TODO - уведомление о загрузке настроек
        settings = SettingsService.get().loadSettings()
        self.__view.showSettings(settings)

    def saveSettinsClick(self, settings: Dict) -> None:
        # TODO - отображение уведомлений о сохранении настроек
        SettingsService.get().saveSettings(settings)
