from __future__ import annotations
from .observer import IEvent, IObserver, IObservable, LoadErrorEvent, LoadDataEvent
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


# Уведомление
class Notification(object):
    message: str = None

    def __init__(self, message: str):
        self.message = message


# Строитель уведомлений
class NotificationBuilder(object):
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

    def build(self) -> List[Notification]:
        if (type(self.__oldItem) is not type(self.__newItem)):
            return []

        notifications: List[Notification] = []
        for notifPropName in self.__notificationProps:
            if hasattr(self.__oldItem, notifPropName):
                oldPropValue = getattr(self.__oldItem, notifPropName)
                newPropValue = getattr(self.__newItem, notifPropName)

                if (oldPropValue == newPropValue):
                    item: NotificationItem = NotificationItem(notifPropName)
                    notifMessage = NotificationItem.configureChangeDisplayValue(item, self.__oldItem, self.__newItem)
                    notifications.append(Notification(notifMessage))

        return notifications


# Событие создания уведомления
class NotificationEvent(IEvent):
    notification: Notification = None

    def __init__(self, notification: Notification):
        super(IEvent, self).__init__()
        self.notification = notification

    def configureEventFromStr(message: str) -> NotificationEvent:
        notification: Notification = Notification(message)
        return NotificationEvent(notification)


# Запись уведомлений в консоль
class ConsoleNotificationObserver(IObserver):
    def __init__(self):
        pass

    def update(self, event: IEvent) -> None:
        if (isinstance(event, NotificationEvent)):
            print(event.notification.message)


# Обработчик уведомлений при загрузке данных, который передаёт уведомления далее
class NotificationObservableObserver(IObserver, IObservable):
    def __init__(self):
        IObserver.__init__(self)
        IObservable.__init__(self)
        self.__notificationBuilder: NotificationBuilder = None
        self.__oldLoadInfo: IInfo = None
        self.__newLoadInfo: IInfo = None

    def update(self, event: IEvent) -> None:
        if (isinstance(event, LoadErrorEvent)):
            errorEvent: LoadErrorEvent = event
            event: NotificationEvent = NotificationEvent.configureEventFromStr(str(errorEvent.error))
            self.notifyObservers(event)

        elif (isinstance(event, LoadDataEvent)):
            loadDataEvent: LoadDataEvent = event
            loadInfo: IInfo = loadDataEvent.info

            if (self.__oldLoadInfo is None):
                self.__oldLoadInfo = loadInfo
                message = f'Осуществлена загрузка данных в {event.loadDate}'
                event: NotificationEvent = NotificationEvent.configureEventFromStr(message)
                self.notifyObservers(event)
                return
            elif (self.__newLoadInfo is None):
                self.__newLoadInfo = loadInfo
                message = f'Осуществлена загрузка данных в {event.loadDate}'
                event: NotificationEvent = NotificationEvent.configureEventFromStr(message)
                self.notifyObservers(event)
            else:
                self.__oldLoadInfo = self.__newLoadInfo
                self.__newLoadInfo = loadInfo
                message = f'Осуществлена загрузка данных в {event.loadDate}'
                event: NotificationEvent = NotificationEvent.configureEventFromStr(message)
                self.notifyObservers(event)

            self.__notificationBuilder = NotificationBuilder(self.__oldLoadInfo, self.__newLoadInfo)
            notifications: List[Notification] = self.__notificationBuilder.build()
            for notification in notifications:
                event: NotificationEvent = NotificationEvent(notification)
                self.notifyObservers(event)

        else:
            raise Exception('Неизвестный тип уведомления')
