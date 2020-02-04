from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import List
from entity.entity import IInfo
from datetime import datetime


class IInfoView(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def showCredentionalView(self) -> None:
        pass


class IInfoPresenter(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def backClick(self) -> None:
        pass
