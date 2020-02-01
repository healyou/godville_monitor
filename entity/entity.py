from typing import List
from abc import ABCMeta


class Pet(object):
    # Вид питомца
    petClass: str = None
    # Уровень питомца (пустая строка, если питомец лишился уровня)
    petLevel: int = None
    # Имя питомца
    petName: str = None
    # Флаг контузии питомца (есть только у контуженого)
    wounded: bool = None

    def __init__(self):
        pass


class IInfo(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass


# Данные открытого API
class OpenApiInfo(IInfo):
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
    # Число собранных слов для книги (без слогов)
    wordsCount: str = None
    # Имя собранного в лаборатории босса
    bossName: str = None
    # Мощь собранного в лаборатории босса
    bossPower: int = None
    # Число собранных тварей женского пола (только у ковчеговладельцев)
    arkFemaleCount: int = None
    # Число собранных тварей мужского пола (только у ковчеговладельцев)
    arkMaleCount: int = None
    # Примерное число сбережений (только у храмовладельцев)
    savings: str = None
    # Уровень героя-торговца (только у лавочников)
    traderLevel: int = None
    # Дата окончания сбора пенсии (только у пенсионеров)
    savingsCompletedAt: str = None
    # Название лавки (только у пенсионеров)
    shopName: str = None
    # Дата окончания храма (только у храмовладельцев)
    templeCompletedAt: str = None
    # Количество поленьев (пока нет храма, ключ отсутствует)
    woodCount: int = None

    def __init__(self):
        super(IInfo, self).__init__()


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
    # Аура героя (без времени; отсутствует без ауры)
    aura: str = None
    # показатель неактуальности данных (ключ появляется, когда данные неактуальны)
    expired: bool = None
    # Тип боя ("sail" - морской поход, "arena" - арена (ЗПГ в том числе), "challenge" - тренировка, "dungeon" - подземелье, "range" - полигон
    fightType: str = None
    # Объект, содержащий описание питомца (подробности ниже)
    pet: Pet = None


    def __init__(self):
        super(PrivateApiInfo, self).__init__()