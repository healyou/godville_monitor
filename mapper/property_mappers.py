from abc import ABCMeta, abstractmethod
from typing import Dict, List


def convertDictKeysToList(dict: Dict) -> List:
    items: List = list()
    for key, value in dict.keys():
        items.append(key)
    return items


def getValueOrDefaultNone(dict: Dict, key: str) -> object:
    return dict.get(key, None)


# абстрактный маппер свойства из словаря
class AbstractDictPropertyMapper(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def mapObject(self, dictValue: Dict, key: str) -> object:
        pass


# Маппер простого значения из словаря
class DefaultDictPropertyMapper(AbstractDictPropertyMapper):
    def __init__(self):
        super(AbstractDictPropertyMapper, self).__init__()

    def mapObject(self, dictValue: Dict, key: str) -> object:
        return getValueOrDefaultNone(dictValue, key)


# Маппер, который для свойства вернёт None
class NoneObjectDictPropertyMapper(AbstractDictPropertyMapper):
    def __init__(self):
        super(AbstractDictPropertyMapper, self).__init__()

    def mapObject(self, dictValue: Dict, key: str) -> object:
        return None


# Маппер листа объектов
class ListDictPropertyMapper(AbstractDictPropertyMapper):
    def __init__(self):
        super(AbstractDictPropertyMapper, self).__init__()

    def mapObject(self, dictValue: Dict, key: str) -> object:
        return convertDictKeysToList(dictValue.get(key, dict()))
