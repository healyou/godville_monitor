from typing import List


# Данные открытого API
class OpenApiInfo(object):
    # Имя героя
    heroName: str = None
    # Имя бога
    godName: str = None
    # Пол
    gender: str = None
    # Уровень героя
    level: int = None
    # Максимальный уровень здоровья
    maxHealth: int = None
    # Максимальный размер инвенторя
    inventoryMaxNum: int = None
    # Девиз
    motto: str = None
    # Имя клана
    clanName: str = None
    # Позиция героя в клане
    clanPosition: str = None
    # Характер героя
    alignment: str = None
    # Количество кирпичей в штуках
    bricksCnt: int = None
    # Дата постройки ковчега
    arkCompletedAt: str = None
    # Счетчик побед на арене
    arenaWonCount: int = None
    # Счетчик поражений на арене
    arenaLostCount: int = None
    # Инвентарь
    inventory: List[str] = None
    # Приблизительное количество золота
    goldApprox: str = None

    def __init__(self):
        pass


# Данные закрытого API
class PrivateApiInfo(OpenApiInfo):
    # TODO - дописать приватные параметры

    def __init__(self):
        super(PrivateApiInfo, self).__init__()