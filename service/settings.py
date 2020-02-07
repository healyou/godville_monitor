from __future__ import annotations
from typing import List
import pickle
from entity.settings import ISetting


class SettingsService(object):
    NOTIF_PROP_FILENAME: str = 'notificationSettings.pkl'

    # Реализация одиночки
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SettingsService, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        pass
        
    def get() -> SettingsService:
        return SettingsService()

    def saveSettings(self, settings: List[ISetting]) -> None:
        self.__saveSettingsToFile(settings)

    def loadSettings(self) -> List[ISetting]:
        return self.__loadSettingsFromFile()

    # TODO - для каждой настройки должно быть своё место, чтобы при очередном сохранении только обновлять уже записанные данные
    # а сейчас всё пересаписывается
    def __saveSettingsToFile(self, settings: List[ISetting]):
        with open(self.NOTIF_PROP_FILENAME, 'wb') as output:  # Overwrites any existing file.
            pickle.dump(settings, output, pickle.HIGHEST_PROTOCOL)

    def __loadSettingsFromFile(self) -> List[ISetting]:
        with open(self.NOTIF_PROP_FILENAME, 'rb') as input:
            return pickle.load(input)
