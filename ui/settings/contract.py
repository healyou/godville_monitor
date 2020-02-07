from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import List
from entity.settings import ISetting, NotificationPropertySetting
from datetime import datetime
from logic.notification_items import NotificationItem
from entity.entity import IInfo, OpenApiInfo, PrivateApiInfo
from typing import Dict, List


class ISettingsView(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def showCredentionalView(self) -> None:
        pass
    @abstractmethod
    def showSettings(self, settings: List[ISetting]) -> None:
        pass
    @abstractmethod
    def showMessage(self, message: str) -> None:
        pass


class ISettingsPresenter(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def afterInitView(self) -> None:
        pass
    @abstractmethod
    def backClick(self) -> None:
        pass
    @abstractmethod
    def saveSettinsClick(self, settings: List[ISetting]) -> None:
        pass
