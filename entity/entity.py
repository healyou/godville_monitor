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
    # Количество здоровья
    health: int = None
    # Процент выполнения квеста 0-100
    questProgress: int = None
    # Процент опыта до следующего уровня 0-100
    expProgress: int = None
    # Количество праны 0-100
    godPower: int = None
    # Последняя запись в дневнике
    diaryLast: str = None
    # Город, в котором герой
    townName: str = None
    # Расстояние от столицы
    distance: int = None
    # Признак сражения на арене
    arenaFight: bool = None
    # Количество вещей в инвентаре
    inventoryNum: int = None
    # Название текущего квеста
    questName: str = None
    # Активируемые трофеи в инвентаре
    activatables: List[str] = None

    def __init__(self):
        super(PrivateApiInfo, self).__init__()