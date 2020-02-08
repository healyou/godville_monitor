from __future__ import annotations
from typing import List
import pickle
from entity.settings import ISetting, NotificationPropertySetting
import json


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if (isinstance(obj, NotificationPropertySetting)):
            propertySetting: NotificationPropertySetting = obj
            from logic.notification_items import NotificationItem
            item: NotificationItem = propertySetting.item
            notify: bool = propertySetting.notify
            return {
                'class': f'{NotificationPropertySetting.__name__}',
                'propertyName': str(item.propertyName),
                'notify': str(notify)
            }
        else:
            return obj.__dict__


class CustomJsonDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if 'class' in obj and obj['class'] == NotificationPropertySetting.__name__:
            from logic.notification_items import NotificationItem
            item: NotificationItem = NotificationItem.getByPropertyName(obj['propertyName'])
            notify: bool = obj['notify'] == 'True'
            return NotificationPropertySetting(item, notify)
        else:
            return obj


class SettingsService(object):
    NOTIF_PROP_FILENAME: str = 'notificationSettings.txt'

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
        value: str = json.dumps(settings, cls=CustomJsonEncoder)
        with open(self.NOTIF_PROP_FILENAME, 'w') as output:  # Overwrites any existing file.
            output.write(value)

    def __loadSettingsFromFile(self) -> List[ISetting]:
        with open(self.NOTIF_PROP_FILENAME, 'r') as input:
            value = input.read()
            return json.loads(value, cls=CustomJsonDecoder)
