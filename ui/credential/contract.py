from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import List
from entity.entity import IInfo
from datetime import datetime


class ICredentionalView(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def showInfoView(self, openInfo: bool) -> None:
        pass
    @abstractmethod
    def showCredentionalError(self, message: str) -> None:
        pass


class ICredentionalPresenter(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def enterCredentional(self, godName: str, token: str) -> None:
        pass
