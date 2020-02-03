from __future__ import annotations
from .observer import IEvent, IObserver, IObservable, LoadErrorEvent, LoadDataEvent, AbstractLoaderEvent
from enum import Enum
from entity.entity import IInfo
from typing import List


class NotificationItem(Enum):
    # Имя героя heroName: str = None
    HERO_NAME = 'heroName'
    # Имя бога godName: str = None
    GOD_NAME = 'godName'
    # Пол gender: str = None
    GENDER = 'gender'

    # Формирование информационного сообщения по изменённому свойству
    def configureChangeDisplayValue(item: NotificationItem, oldItem: IInfo, newItem: IInfo) -> str:
        oldPropValue = getattr(oldItem, item.value)
        newPropValue = getattr(newItem, item.value)

        displayValue: str = None

        if (item == NotificationItem.HERO_NAME):
            displayValue = f'Изменилось имя героя с {oldPropValue} на {newPropValue}'
        elif (item == NotificationItem.GOD_NAME):
            displayValue = f'Изменилось имя бога с {oldPropValue} на {newPropValue}'
        elif (item == NotificationItem.GENDER):
            displayValue = f'Изменился пол героя с {oldPropValue} на {newPropValue}'
        else:
            raise Exception('Незвестное свойство')

        return displayValue 


# Строитель уведомлений
class NotificationEventBuilder(object):
    def __init__(self, oldItem: IInfo, newItem: IInfo):
        self.__oldItem: IInfo = oldItem
        self.__newItem: IInfo = newItem
        # TODO - фильтр на уведомления
        self.__notificationProps: List[str] = self.__configureNotificationProps()

    def __configureNotificationProps(self) -> List[str]:
        notificationProps: List[str] = []
        for item in NotificationItem:
            notificationProps.append(item.value)
        return notificationProps

    def build(self) -> List[NotificationEvent]:
        if (type(self.__oldItem) is not type(self.__newItem)):
            return []

        notifications: List[NotificationEvent] = []
        for notifPropName in self.__notificationProps:
            if hasattr(self.__oldItem, notifPropName):
                oldPropValue = getattr(self.__oldItem, notifPropName)
                newPropValue = getattr(self.__newItem, notifPropName)

                if (oldPropValue == newPropValue):
                    item: NotificationItem = NotificationItem(notifPropName)
                    notifMessage = NotificationItem.configureChangeDisplayValue(item, self.__oldItem, self.__newItem)
                    notifications.append(NotificationEvent(notifMessage))

        return notifications


# Событие создания уведомления
class NotificationEvent(IEvent):
    message: str = None

    def __init__(self, message: str):
        super(IEvent, self).__init__()
        self.message = message


# Запись уведомлений в консоль
class ConsoleNotificationObserver(IObserver):
    def __init__(self):
        pass

    def update(self, event: IEvent) -> None:
        if (isinstance(event, NotificationEvent)):
            print(event.message)


# Обработчик уведомлений при загрузке данных, который передаёт уведомления далее
class NotificationObservableObserver(IObserver, IObservable):
    def __init__(self):
        IObserver.__init__(self)
        IObservable.__init__(self)
        self.__oldLoadInfo: IInfo = None
        self.__newLoadInfo: IInfo = None

    def update(self, event: IEvent) -> None:
        if (not isinstance(event, AbstractLoaderEvent)):
            return

        notifications: List[NotificationEvent] = self.__configureNotificationEvents(event)
        self.__notifyNotifications(notifications)

    def __configureNotificationEvents(self, event: IEvent) -> List[NotificationEvent]:
        notifications: List[NotificationEvent] = []

        if (isinstance(event, LoadErrorEvent)):
            notifications.append(self.__configureLoadErrorNotificationEvent(event))

        elif (isinstance(event, LoadDataEvent)):
            loadDataEvent: LoadDataEvent = event
            loadInfo: IInfo = loadDataEvent.info

            if (self.__oldLoadInfo is None):
                self.__oldLoadInfo = loadInfo
                notifications.append(self.__configureLoadDataNotificationEvent(event))
                return notifications

            elif (self.__newLoadInfo is None):
                self.__newLoadInfo = loadInfo
                notifications.append(self.__configureLoadDataNotificationEvent(event))

            else:
                self.__oldLoadInfo = self.__newLoadInfo
                self.__newLoadInfo = loadInfo
                notifications.append(self.__configureLoadDataNotificationEvent(event))

            propEvents: List[NotificationEvent] = self.__configureChangedPropertiesNotificationEvents(self.__oldLoadInfo, self.__newLoadInfo)
            notifications.extend(propEvents)
        
        return notifications

    def __configureLoadErrorNotificationEvent(self, event: LoadErrorEvent) -> NotificationEvent:
        message = f'Осуществлена загрузка данных в {event.loadDate}'
        return NotificationEvent(message)

    def __configureLoadDataNotificationEvent(self, event: LoadDataEvent) -> NotificationEvent:
        message = f'Осуществлена загрузка данных в {event.loadDate}'
        return NotificationEvent(message)

    def __notifyNotifications(self, notifications: List[NotificationEvent]):
        for event in notifications:
            self.notifyObservers(event)

    def __configureChangedPropertiesNotificationEvents(self, oldLoadInfo: IInfo, newLoadInfo: IInfo) -> List[NotificationEvent]:
        notificationBuilder = NotificationEventBuilder(oldLoadInfo, newLoadInfo)
        return notificationBuilder.build()
