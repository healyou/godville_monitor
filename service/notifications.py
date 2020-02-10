from __future__ import annotations
from logic.notification import NotificationEvent
from typing import List


class NotificationService(object):
    __notificationsHistory: List[NotificationEvent] = []

    # Реализация одиночки
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(NotificationService, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        pass

    def get() -> NotificationService:
        return NotificationService()

    def addNotificationEventToHistory(self, event: NotificationEvent):
        self.__notificationsHistory.append(event)

    def getFirstSavedEvent(self) -> NotificationEvent:
        if self.__notificationsHistory:
            return self.__notificationsHistory.pop(0)
        else:
            return None
