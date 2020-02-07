from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import List
from entity.entity import IInfo
from datetime import datetime
from logic.notification_items import NotificationItem
from entity.entity import IInfo, OpenApiInfo, PrivateApiInfo


class IInfoView(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def showCredentionalView(self) -> None:
        pass
    @abstractmethod
    def showChangedPropertiesInfo(self, item: NotificationItem, value: str) -> None:
        pass
    @abstractmethod
    def showLoadDataInfo(self, message: str) -> None:
        pass


class IInfoPresenter(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def backClick(self) -> None:
        pass
    @abstractmethod
    def afterInitView(self) -> None:
        pass
