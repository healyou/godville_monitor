from tkinter import *
from .contract import ISettingsView, ISettingsPresenter
from typing import List, Dict
from entity.settings import ISetting, NotificationPropertySetting
from logic.notification import IEvent, NotificationEvent, LoadDataEvent, LoadErrorEvent, ChangePropertiesNotificationEvent
from logic.notification_items import NotificationItem
from ui.component.scrollableframe import VerticalScrolledFrame
from service.settings import SettingsService
from datetime import datetime


class SettingsView(ISettingsView):
    __presenter: ISettingsPresenter = None
    __root: Tk = None
    __frame: Frame = None
    __checkSettingBooleanVars: Dict = {}
    __infoLabel: Label = None

    def __init__(self, root: Tk):
        ISettingsView.__init__(self)
        self.__presenter = SettingsPresenter(self)
        self.__root = root
        self.__initFrame()
        self.__presenter.afterInitView()

    def __initFrame(self):
        self.__clearChildrens()

        # TODO добавить скролл
        self.__frame = Frame(master=self.__root, bd=1, relief=SUNKEN)
        self.__frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        self.__infoLabel = Label(master=self.__frame, text='Ещё не было загрузки настроек')
        self.__infoLabel.pack(side=TOP, padx=5, pady=5)

        i: int = 1
        # TODO - все настройки можно редактировать
        for notifItem in [NotificationItem.GOD_NAME, NotificationItem.HERO_NAME, NotificationItem.HEALTH]:
            frame = Frame(master=self.__frame, bd=1, relief=SUNKEN)
            frame.pack(side=TOP, fill=X, expand=True)

            notify: bool = False
            settingVar = BooleanVar()
            settingVar.set(notify)
            settingCheckBox = Checkbutton(master=frame, text=notifItem.propertyName, variable=settingVar, onvalue=True, offvalue=False)
            settingCheckBox.pack(side=TOP, padx=5)
            self.__checkSettingBooleanVars[notifItem] = settingVar
            # TODO - приватное или открытое свойство
            i += 1

        enterButton = Button(master=self.__frame, text='Назад', command=self.__onBackClick)
        enterButton.pack(side=TOP, padx=5, pady=5)

        saveButton = Button(master=self.__frame, text='Сохранить', command=self.__onSaveSetingsClick)
        saveButton.pack(side=TOP, padx=5, pady=5)

    def __onBackClick(self):
        self.__presenter.backClick()

    def __onSaveSetingsClick(self):
        settings: List[NotificationPropertySetting] = []
        for key in self.__checkSettingBooleanVars:
            item: NotificationItem = key
            notify: bool = self.__checkSettingBooleanVars[item].get()
            settings.append(NotificationPropertySetting(item, notify))

        self.__presenter.saveSettinsClick(settings)

    def __clearChildrens(self):
        for widget in self.__root.winfo_children():
            widget.destroy()

    def showCredentionalView(self) -> None:
        from ui.credential.credentional import CredentionalView
        CredentionalView(self.__root)

    def showSettings(self, settings: List[ISetting]) -> None:
        for setting in settings:
            item: NotificationItem = setting.item
            notify: bool = setting.notify

            value: BooleanVar = self.__checkSettingBooleanVars[item]
            value.set(setting.notify)

    def showMessage(self, message: str) -> None:
        self.__infoLabel.config(text=message)


class SettingsPresenter(ISettingsPresenter):
    __view: ISettingsView = None

    def __init__(self, view: ISettingsView):
        ISettingsPresenter.__init__(self)
        self.__view = view

    def backClick(self) -> None:
        self.__view.showCredentionalView()

    def afterInitView(self) -> None:
        try:
            settings: List[NotificationPropertySetting] = SettingsService.get().loadSettings()
            self.__view.showSettings(settings)
            self.__view.showMessage(f'Настройки успешно загружены: {str(datetime.now())}')
        except Exception as err:
            self.__view.showMessage(f'Ошибка загрузки настроек: {str(err)}')

    def saveSettinsClick(self, settings: List[ISetting]) -> None:
        try:
            SettingsService.get().saveSettings(settings)
            # savedSettings: List[ISetting] = SettingsService.get().loadSettings()
            # self.__view.showSettings(savedSettings)
            # self.__view.showMessage(f'Настройки успешно сохранены: {str(datetime.now())}')
            self.__view.showCredentionalView()
        except Exception as err:
            self.__view.showMessage(f'Ошибка сохранения настроек: {str(err)}')
