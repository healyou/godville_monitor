from tkinter import *
from .contract import IInfoPresenter, IInfoView
from typing import List, Dict
from entity.entity import OpenApiInfo, PrivateApiInfo
from logic.session import Session
from logic.observer import IObserver
from logic.notification import IEvent, NotificationEvent, LoadDataEvent, LoadErrorEvent, ChangePropertiesNotificationEvent
from logic.notification_items import NotificationItem
from ui.component.scrollableframe import VerticalScrolledFrame
from logic.filter import GuiPropNotificationFilter


class InfoView(IInfoView):
    __presenter: IInfoPresenter = None
    __root: Tk = None
    __frame: Frame = None
    __loadDataLabel: Label = None
    __infoLabels: Dict = {}

    def __init__(self, root: Tk):
        IInfoView.__init__(self)
        self.__presenter = InfoPresenter(self)
        self.__root = root
        self.__initFrame()
        self.__presenter.afterInitView()

    def __initFrame(self):
        self.__clearChildrens()

        self.__frame = Frame(master=self.__root, bd=1, relief=SUNKEN)
        self.__frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        self.__loadDataLabel = Label(master=self.__root, text='Ещё не было загрузки данных')
        self.__loadDataLabel.pack(side=TOP,  fill=BOTH, expand=True, padx=5, pady=5)

        i: int = 1
        propFilter: GuiPropNotificationFilter = GuiPropNotificationFilter.get()
        notifPropItems: List[NotificationItem] = propFilter.getAvailablenotificationItems()
        for notifItem in notifPropItems:
            frame = Frame(master=self.__frame, bd=1, relief=SUNKEN)
            frame.pack(side=TOP, fill=BOTH, expand=True)

            propLabel = Label(master=frame, text=notifItem.propertyName)
            propLabel.pack(side=LEFT, padx=5)
            propValueLabel = Label(master=frame, name=notifItem.propertyName, text='None')
            propValueLabel.pack(side=RIGHT, padx=5)
            self.__infoLabels[notifItem.propertyName] = propValueLabel
            i += 1

        enterButton = Button(master=self.__frame, text='Назад', command=self.__onBackClick)
        enterButton.pack(side=TOP, padx=5, pady=5)

    def __onBackClick(self):
        self.__presenter.backClick()

    def __clearChildrens(self):
        for widget in self.__root.winfo_children():
            widget.destroy()

    def showCredentionalView(self) -> None:
        from ui.credential.credentional import CredentionalView
        CredentionalView(self.__root)

    def showChangedPropertiesInfo(self, item: NotificationItem, value: str) -> None:
        self.__infoLabels[item.propertyName]['text'] = value

    def showLoadDataInfo(self, message: str) -> None:
        self.__loadDataLabel['text'] = message


class InfoPresenter(IInfoPresenter, IObserver):
    __view: IInfoView = None
    __loadedData: bool = False

    def __init__(self, view: IInfoView):
        IInfoPresenter.__init__(self)
        IObserver.__init__(self)
        self.__view = view

        self.__firstNotif: bool = True

    def backClick(self) -> None:
        Session.get().stopLoadData()
        self.__view.showCredentionalView()

    def update(self, event: IEvent) -> None:
        if (isinstance(event, NotificationEvent)):
            event: NotificationEvent = event
                
            notifTitle: str = 'Godville следилка'
            notifMessage: str = ''
            for message in event.messages:
                if notifMessage:
                    notifMessage += '\n'
                notifMessage += message
            
            Session.get().showNotification(notifTitle, notifMessage)    

        elif (isinstance(event, ChangePropertiesNotificationEvent)):
            changePropEvent: ChangePropertiesNotificationEvent = event
            item: NotificationItem = changePropEvent.notificationItem
            value: str = str(changePropEvent.newValue)
            self.__view.showChangedPropertiesInfo(item, value)

        elif (isinstance(event, LoadDataEvent)):
            if (not self.__loadedData):
                self.__loadedData = True
                self.__initFirstLoadData(event)

            message: str = self.__configureLoadDataEventMessage(event)
            self.__view.showLoadDataInfo(message)

        elif (isinstance(event, LoadErrorEvent)):
            loadDataEvent: LoadErrorEvent = event
            error: Exception = loadDataEvent.error
            loadDate: datetime = loadDataEvent.loadDate
            message: str = f'Ошибка во время последнего обновления данных {str(loadDate)}: {str(error)}'
            self.__view.showLoadDataInfo(message)

    def afterInitView(self) -> None:
        Session.get().startLoadData([self])
        lastLoadData: LoadDataEvent = Session.get().getLastLoadData()
        if (lastLoadData is not None):
            self.__initFirstLoadData(lastLoadData)

    def __initFirstLoadData(self, lastLoadData: LoadDataEvent):
        self.__loadedData = True
        message: str = self.__configureLoadDataEventMessage(lastLoadData)
        self.__view.showLoadDataInfo(message)

        info: IInfo = lastLoadData.info
        notificatioItems: List[NotificationItem] = GuiPropNotificationFilter.get().getAvailablenotificationItems()
        for item in notificatioItems:
            value: str = str(getattr(info, item.propertyName))
            self.__view.showChangedPropertiesInfo(item, value)

    def __configureLoadDataEventMessage(self, loadDataEvent: LoadDataEvent) -> str:
        isPrivateInfo: bool = isinstance(loadDataEvent.info, PrivateApiInfo)
        openMessage: str = None
        if (isPrivateInfo):
            openMessage = 'закрытых'
        else:
            openMessage = 'открытых'
        loadDate: datetime = loadDataEvent.loadDate
        return f'Время последнего обновления {openMessage} данных {str(loadDate)}'
