from __future__ import annotations

from collections import namedtuple
from enum import Enum
from typing import List
from threading import Lock

from entity.entity import IInfo, OpenApiInfo, PrivateApiInfo
from mapper.property_mappers import (AbstractDictPropertyMapper,
                                     DefaultDictPropertyMapper,
                                     NoneObjectDictPropertyMapper)

from .filter import GuiPropNotificationFilter, UserPropNotificationFilter
from .notification_items import NotificationItem
from .observer import (AbstractLoaderEvent, IEvent, IObservable, IObserver,
                       LoadDataEvent, LoadErrorEvent)


# Событие создания уведомления
class NotificationEvent(IEvent):
    messages: List[str] = []

    def __init__(self, messages: List[str]):
        super(IEvent, self).__init__()
        self.messages = messages


class ChangePropertiesNotificationEvent(IEvent):
    notificationItem: NotificationItem = None
    oldValue: object = None
    newValue: object = None

    def __init__(self, notificationItem: NotificationItem, oldValue: object, newValue: object):
        super(IEvent, self).__init__()
        self.notificationItem = notificationItem
        self.oldValue = oldValue
        self.newValue = newValue


# Строитель уведомлений
class NotificationEventBuilder(object):
    def __init__(self, oldItem: IInfo, newItem: IInfo):
        self.__oldItem: IInfo = oldItem
        self.__newItem: IInfo = newItem
        self.__guiNotificationFilter: GuiPropNotificationFilter = GuiPropNotificationFilter.get()
        self.__userPropNotificationfilter: UserPropNotificationFilter = UserPropNotificationFilter.get()

    def build(self) -> List[NotificationEvent]:
        if (type(self.__oldItem) is not type(self.__newItem)):
            return []

        notifications: List[NotificationEvent] = []
        notificationMessages: List[str] = []
        for notifItem in NotificationItem:
            notifPropName: str = notifItem.propertyName
            if hasattr(self.__oldItem, notifPropName):
                oldPropValue = getattr(self.__oldItem, notifPropName)
                newPropValue = getattr(self.__newItem, notifPropName)

                if (oldPropValue == newPropValue):
                    if (self.__guiNotificationFilter.isNotificationCreate(notifItem)):
                        event: ChangePropertiesNotificationEvent = ChangePropertiesNotificationEvent(notifItem, oldPropValue, newPropValue)
                        notifications.append(event)

                    if (self.__userPropNotificationfilter.isNotificationCreate(notifItem)):
                        notifMessage = NotificationItem.configureChangeDisplayValue(notifItem, self.__oldItem, self.__newItem)
                        notificationMessages.append(notifMessage)

        if notificationMessages:
            event: NotificationEvent = NotificationEvent(notificationMessages)
            notifications.append(NotificationEvent(notificationMessages))
            from service.notifications import NotificationService
            NotificationService.get().addNotificationEventToHistory(event)

        return notifications


# Запись уведомлений в консоль
class ConsoleNotificationObserver(IObserver):
    def __init__(self):
        super(IObserver, self).__init__()

    def update(self, event: IEvent) -> None:
        if (isinstance(event, NotificationEvent)):
            print(event.messages)


# Обработчик уведомлений с возможностью остановки работы
class UiNotificationObserver(IObserver):
    __mutex = Lock()
    __uiObserver: IObserver = None

    def __init__(self):
        super(IObserver, self).__init__()

    def setUiObserver(self, observer: IObserver):
        self.__mutex.acquire()
        try:
            self.__uiObserver = observer
        finally:
            self.__mutex.release()

    def clearUiObserver(self):
        self.__mutex.acquire()
        try:
            self.__uiObserver = None
        finally:
            self.__mutex.release()

    def update(self, event: IEvent) -> None:
        if self.__uiObserver:
            self.__mutex.acquire()
            try:
                self.__uiObserver.update(event)
            finally:
                self.__mutex.release()


# Обработчик уведомлений при загрузке данных, который передаёт уведомления далее
class NotificationObservableObserver(IObserver, IObservable):
    def __init__(self):
        IObserver.__init__(self)
        IObservable.__init__(self)
        self.__oldLoadInfo: IInfo = None
        self.__newLoadInfo: IInfo = None

        from logic.session import Session
        session: Session = Session.get()
        lastLoadData: LoadDataEvent = session.getLastLoadData()
        if (lastLoadData is not None):
            if (session.isLoadPrivateInfo() and isinstance(lastLoadData.info, PrivateApiInfo)):
                self.__oldLoadInfo = lastLoadData.info
            elif (not session.isLoadPrivateInfo() and isinstance(lastLoadData.info, OpenApiInfo)):
                self.__oldLoadInfo = lastLoadData.info

    def update(self, event: IEvent) -> None:
        if (not isinstance(event, AbstractLoaderEvent)):
            return

        notifications: List[NotificationEvent] = self.__configureNotificationEvents(event)
        self.__notifyNotifications(notifications)

    def __configureNotificationEvents(self, event: IEvent) -> List[NotificationEvent]:
        notifications: List[NotificationEvent] = []

        if (isinstance(event, LoadErrorEvent)):
            notifications.append(event)
            # notifications.append(self.__configureLoadErrorNotificationEvent(event))

        elif (isinstance(event, LoadDataEvent)):
            from logic.session import Session
            Session.get().setLastLoadData(event)

            notifications.append(event)
            loadDataEvent: LoadDataEvent = event
            loadInfo: IInfo = loadDataEvent.info

            if (self.__oldLoadInfo is None):
                self.__oldLoadInfo = loadInfo
                # notifications.append(self.__configureLoadDataNotificationEvent(event))
                return notifications

            elif (self.__newLoadInfo is None):
                self.__newLoadInfo = loadInfo
                # notifications.append(self.__configureLoadDataNotificationEvent(event))

            else:
                self.__oldLoadInfo = self.__newLoadInfo
                self.__newLoadInfo = loadInfo
                # notifications.append(self.__configureLoadDataNotificationEvent(event))

            propEvents: List[NotificationEvent] = self.__configureChangedPropertiesNotificationEvents(self.__oldLoadInfo, self.__newLoadInfo)
            notifications.extend(propEvents)
        
        return notifications

    def __configureLoadErrorNotificationEvent(self, event: LoadErrorEvent) -> NotificationEvent:
        message = f'Ошибка загрузки данных в {event.loadDate}: {event.error}'
        return NotificationEvent([message])

    def __configureLoadDataNotificationEvent(self, event: LoadDataEvent) -> NotificationEvent:
        isPrivateInfo: bool = isinstance(event.info, PrivateApiInfo)
        openMessage: str = None
        if (isPrivateInfo):
            openMessage = 'закрытых'
        else:
            openMessage = 'открытых'
        message = f'Осуществлена загрузка {openMessage} данных в {event.loadDate}: {event.info.__dict__}'
        return NotificationEvent([message])

    def __notifyNotifications(self, notifications: List[NotificationEvent]):
        for event in notifications:
            self.notifyObservers(event)

    def __configureChangedPropertiesNotificationEvents(self, oldLoadInfo: IInfo, newLoadInfo: IInfo) -> List[NotificationEvent]:
        notificationBuilder = NotificationEventBuilder(oldLoadInfo, newLoadInfo)
        return notificationBuilder.build()
