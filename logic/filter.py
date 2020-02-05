from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import List
from .notification_items import NotificationItem


# Фильтр изменения свойств для создания уведомлений
class AbstractPropertiesNotificationFilter(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def isNotificationCreate() -> bool:
        pass


def getAvailablenotificationItems(items: List[NotificationItem]) -> List[NotificationItem]:
    from .session import Session
    loadPrivateInfo: bool = Session.get().isLoadPrivateInfo()
    if (loadPrivateInfo):
        return items
    else:
        availableItems: List[NotificationItem] = []
        for item in items:
            if item.isOpenInfo:
                availableItems.append(item)
        return availableItems

# Изменения свойст, для которых надо создавать уведомления
class GuiPropNotificationFilter(AbstractPropertiesNotificationFilter):
    # TODO - multitheading list
    # TODO - приватная и открытая инфа отдельно
    __notificationItems: List[NotificationItem] = [
        NotificationItem.GOD_NAME, 
        NotificationItem.HERO_NAME,
        NotificationItem.MOTTO,
        NotificationItem.ALIGMENT,
        NotificationItem.CLAN,
        NotificationItem.EXPIRED,
        NotificationItem.BOSS_POWER,
        NotificationItem.ARK_COMPLATED_AT,
        NotificationItem.GOLD_APPROX,
        NotificationItem.MAX_HEALTH,
        NotificationItem.HEALTH,
        NotificationItem.LEVEL,
        NotificationItem.INVENTORY_MAX_NUM,
        NotificationItem.INVENTORY
    ]

    def get() -> GuiPropNotificationFilter:
        return GuiPropNotificationFilter()

    # Реализация одиночки
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GuiPropNotificationFilter, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        super(AbstractPropertiesNotificationFilter, self).__init__()

    def isNotificationCreate(self, item: NotificationItem) -> bool:
        return item in self.getAvailablenotificationItems()

    def getAvailablenotificationItems(self) -> List[NotificationItem]:
        return getAvailablenotificationItems(self.__notificationItems)


# Фильтр изменения свойст, которые увидит пользователь
class UserPropNotificationFilter(AbstractPropertiesNotificationFilter):
    # TODO - multitheading list
    __notificationItems: List[NotificationItem] = [
        NotificationItem.GOD_NAME,
        NotificationItem.HEALTH
    ]

    def get() -> UserPropNotificationFilter:
        return UserPropNotificationFilter()

    # Реализация одиночки
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(UserPropNotificationFilter, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        super(AbstractPropertiesNotificationFilter, self).__init__()

    def isNotificationCreate(self, item: NotificationItem) -> bool:
        return item in self.getAvailablenotificationItems()

    def getAvailablenotificationItems(self) -> List[NotificationItem]:
        return getAvailablenotificationItems(self.__notificationItems)
