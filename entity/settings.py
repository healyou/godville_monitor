from abc import ABCMeta
from logic.notification_items import NotificationItem


class ISetting(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass


# Настройка отправки уведомлений
class NotificationPropertySetting(ISetting):
    item: NotificationItem = None
    notify: bool = None

    def __init__(self, item: NotificationItem, notify: bool):
        ISetting.__init__(self)
        self.item = item
        self.notify = notify
