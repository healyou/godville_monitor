from __future__ import annotations
from mapper.property_mappers import AbstractDictPropertyMapper, DefaultDictPropertyMapper, NoneObjectDictPropertyMapper, ListDictPropertyMapper
from enum import Enum
from collections import namedtuple


NotificationProperty = namedtuple('NotificationProperty', ['propertyName', 'jsonPropName', 'mapper', 'openInfo', 'description'])

class NotificationItem(Enum):
    @property
    def propertyName(self) -> str:
        return self.value.propertyName
    @property
    def jsonPropName(self) -> str:
        return self.value.jsonPropName
    @property
    def isOpenInfo(self) -> bool:
        return self.value.openInfo
    @property
    def description(self) -> str:
        return self.value.description
    @property
    def mapper(self) -> AbstractDictPropertyMapper:
        return self.value.mapper


    # Информация открытого API
    HERO_NAME = NotificationProperty('heroName', 'name', DefaultDictPropertyMapper(), True, 'description')
    GOD_NAME = NotificationProperty('godName', 'godname', DefaultDictPropertyMapper(), True, 'description')
    GENDER = NotificationProperty('gender', 'gender', DefaultDictPropertyMapper(), True, 'description')
    LEVEL = NotificationProperty('level', 'level', DefaultDictPropertyMapper(), True, 'description')
    MAX_HEALTH = NotificationProperty('maxHealth', 'max_health', DefaultDictPropertyMapper(), True, 'description')
    INVENTORY_MAX_NUM = NotificationProperty('inventoryMaxNum', 'inventory_max_num', DefaultDictPropertyMapper(), True, 'description')
    MOTTO = NotificationProperty('motto', 'motto', DefaultDictPropertyMapper(), True, 'description')
    CLAN = NotificationProperty('clan', 'clan', DefaultDictPropertyMapper(), True, 'description')
    CLAN_POSITION = NotificationProperty('clanPosition', 'clan_position', DefaultDictPropertyMapper(), True, 'description')
    ALIGMENT = NotificationProperty('alignment', 'alignment', DefaultDictPropertyMapper(), True, 'description')
    BRICKS_CNT = NotificationProperty('bricksCnt', 'bricks_cnt', DefaultDictPropertyMapper(), True, 'description')
    ARK_COMPLATED_AT = NotificationProperty('arkCompletedAt', 'ark_completed_at', DefaultDictPropertyMapper(), True, 'description')
    ARENA_WON_COUNT = NotificationProperty('arenaWonCount', 'arena_won', DefaultDictPropertyMapper(), True, 'description')
    ARENA_LOST_COUNT = NotificationProperty('arenaLostCount', 'arena_lost', DefaultDictPropertyMapper(), True, 'description')
    GOLD_APPROX = NotificationProperty('gold_approx', 'gold_approx', DefaultDictPropertyMapper(), True, 'description')
    INVENTORY = NotificationProperty('inventory', 'inventory', ListDictPropertyMapper(), True, 'description')
    WORDS_COUNT = NotificationProperty('wordsCount', 'words', DefaultDictPropertyMapper(), True, 'description')
    BOSS_NAME = NotificationProperty('bossName', 'boss_name', DefaultDictPropertyMapper(), True, 'description')
    BOSS_POWER = NotificationProperty('bossPower', 'boss_power', DefaultDictPropertyMapper(), True, 'description')
    ARC_FEMALE_COUNT = NotificationProperty('arkFemaleCount', 'ark_f', DefaultDictPropertyMapper(), True, 'description')
    ARC_MALE_COUNT = NotificationProperty('arkMaleCount', 'ark_m', DefaultDictPropertyMapper(), True, 'description')
    SAVINGS = NotificationProperty('savings', 'savings', DefaultDictPropertyMapper(), True, 'description')
    TRADER_LEVEL = NotificationProperty('traderLevel', 't_level', DefaultDictPropertyMapper(), True, 'description')
    SAVINGS_COMPLATE_AT = NotificationProperty('savingsCompletedAt', 'savings_completed_at', DefaultDictPropertyMapper(), True, 'description')
    SHOP_NAME = NotificationProperty('shopName', 'shop_name', DefaultDictPropertyMapper(), True, 'description')
    TEMPLE_COMPLATED_AT = NotificationProperty('templeCompletedAtender', 'temple_completed_at', DefaultDictPropertyMapper(), True, 'description')
    WOOD_COUNT = NotificationProperty('woodCount', 'wood_cnt', DefaultDictPropertyMapper(), True, 'description')

    # Информация закрытого API
    HEALTH = NotificationProperty('health', 'health', DefaultDictPropertyMapper(), False, 'description')
    QUEST_PROGRESS = NotificationProperty('questProgress', 'quest_progress', DefaultDictPropertyMapper(), False, 'description')
    EXP_PROGRESS = NotificationProperty('expProgress', 'exp_progress', DefaultDictPropertyMapper(), False, 'description')
    GOD_POWER = NotificationProperty('godPower', 'godpower', DefaultDictPropertyMapper(), False, 'description')
    DIARY_LAST = NotificationProperty('diaryLast', 'diary_last', DefaultDictPropertyMapper(), False, 'description')
    TOWN_NAME = NotificationProperty('townName', 'town_name', DefaultDictPropertyMapper(), False, 'description')
    DISTANCE = NotificationProperty('distance', 'distance', DefaultDictPropertyMapper(), False, 'description')
    ARENA_FIGHT = NotificationProperty('arenaFight', 'arena_fight', DefaultDictPropertyMapper(), False, 'description')
    INVETORY_NUM = NotificationProperty('inventoryNum', 'inventory_num', DefaultDictPropertyMapper(), False, 'description')
    QUEST_NAME = NotificationProperty('questName', 'quest', DefaultDictPropertyMapper(), False, 'description')
    ACTIVATABLES = NotificationProperty('activatables', 'activatables', DefaultDictPropertyMapper(), False, 'description')
    AURA = NotificationProperty('aura', 'aura', DefaultDictPropertyMapper(), False, 'description')
    EXPIRED = NotificationProperty('expired', 'expired', DefaultDictPropertyMapper(), False, 'description')
    FIGHT_TYPE = NotificationProperty('fightType', 'fight_type', DefaultDictPropertyMapper(), False, 'description')
    PET = NotificationProperty('pet', 'pet', NoneObjectDictPropertyMapper(), False, 'description')

    def getByPropertyName(propertyName: str) -> NotificationItem:
        for item in NotificationItem:
            if item.propertyName == propertyName:
                return item
        raise Exception('Элемент не найден')

    # Формирование информационного сообщения по изменённому свойству
    def configureChangeDisplayValue(item: NotificationItem, oldItem: IInfo, newItem: IInfo) -> str:
        oldPropValue = getattr(oldItem, item.propertyName)
        newPropValue = getattr(newItem, item.propertyName)

        displayValue: str = None

        if (item == NotificationItem.HERO_NAME):
            displayValue = f'Изменилось имя героя с \'{oldPropValue}\' на \'{newPropValue}\''
        elif (item == NotificationItem.GOD_NAME):
            displayValue = f'Изменилось имя бога с \'{oldPropValue}\' на \'{newPropValue}\''
        elif (item == NotificationItem.GENDER):
            displayValue = f'Изменился пол героя с \'{oldPropValue}\' на \'{newPropValue}\''
        else:
            displayValue = f'Изменилось неизвестное свойство с \'{oldPropValue}\' на \'{newPropValue}\''

        return displayValue 
