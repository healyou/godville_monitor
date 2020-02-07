from __future__ import annotations
from typing import Dict


class SettingsService(object):
    # Реализация одиночки
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SettingsService, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        pass
        
    def get() -> SettingsService:
        return SettingsService()

    # TODO - формат настроей для сохранения
    def saveSettings(self, settings: Dict) -> None:
        # TODO - сохранение и загрузка настроек из бд
        pass

    def loadSettings(self) -> Dict:
        return {}
