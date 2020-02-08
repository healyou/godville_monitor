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


# Получить параметры относительно того, что можно грузить пользователю
def getAvailablePrivateOrOpenInfo(items: List[NotificationItem]) -> List[NotificationItem]:
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
        return getAvailablePrivateOrOpenInfo(self.__notificationItems)


# Фильтр изменения свойст, которые увидит пользователь
class UserPropNotificationFilter(AbstractPropertiesNotificationFilter):
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
        notificationItems: List[NotificationItem] = self.__getUserSavedNotificationItems()
        return getAvailablePrivateOrOpenInfo(notificationItems)

    # Получить свойства, которые нужны для уведомлений пользователю (сохранены пользвателем)
    def __getUserSavedNotificationItems(self):
        from .session import Session
        from entity.settings import ISetting, NotificationPropertySetting
        settings: List[ISetting] = Session.get().getUserSettings()
        availableItems: List[NotificationItem] = []
        for setting in settings:
            if isinstance(setting, NotificationPropertySetting):
                if setting.notify:
                    availableItems.append(setting.item)
        return availableItems
