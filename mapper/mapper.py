import json
from typing import List, Dict
from collections import namedtuple
from entity.entity import OpenApiInfo, PrivateApiInfo


def convertDictKeysToList(dict: Dict) -> List:
    items: List = list()
    for key, value in dict.keys():
        items.append(key)
    return items


def getValueOrDefaultNone(dict: Dict, key: str) -> object:
    return dict.get(key, None)


class OpenApiInfoMapper(object):
    def __init__(self):
        pass

    def mapObject(self, jsonData: str) -> OpenApiInfo:
        objInfo = json.loads(jsonData)

        info = OpenApiInfo()
        info.godName = getValueOrDefaultNone(objInfo, 'godname')
        info.heroName = getValueOrDefaultNone(objInfo, 'name')
        info.gender = getValueOrDefaultNone(objInfo, 'gender')
        info.level = getValueOrDefaultNone(objInfo, 'level')
        info.maxHealth = getValueOrDefaultNone(objInfo, 'max_health')
        info.inventoryMaxNum = getValueOrDefaultNone(objInfo, 'inventory_max_num')
        info.motto = getValueOrDefaultNone(objInfo, 'motto')
        info.clan = getValueOrDefaultNone(objInfo, 'clan')
        info.clanPosition = getValueOrDefaultNone(objInfo, 'clan_position')
        info.alignment = getValueOrDefaultNone(objInfo, 'alignment')
        info.bricksCnt = getValueOrDefaultNone(objInfo, 'bricks_cnt')
        info.arkCompletedAt = getValueOrDefaultNone(objInfo, 'ark_completed_at')
        info.arenaWonCount = getValueOrDefaultNone(objInfo, 'arena_won')
        info.arenaLostCount = getValueOrDefaultNone(objInfo, 'arena_lost')
        info.gold_approx = getValueOrDefaultNone(objInfo, 'gold_approx')
        # Приходит список, а в python воспринимается как словарь
        info.inventory = convertDictKeysToList(objInfo.get('inventory', dict()))
        info.wordsCount = getValueOrDefaultNone(objInfo, 'words')
        info.bossName = getValueOrDefaultNone(objInfo, 'boss_name')
        info.bossPower = getValueOrDefaultNone(objInfo, 'boss_power')
        info.arkFemaleCount = getValueOrDefaultNone(objInfo, 'ark_f')
        info.arkMaleCount = getValueOrDefaultNone(objInfo, 'ark_m')
        info.savings = getValueOrDefaultNone(objInfo, 'savings')
        info.traderLevel = getValueOrDefaultNone(objInfo, 't_level')
        info.savingsCompletedAt = getValueOrDefaultNone(objInfo, 'savings_completed_at')
        info.shopName = getValueOrDefaultNone(objInfo, 'shop_name')
        info.templeCompletedAt = getValueOrDefaultNone(objInfo, 'temple_completed_at')
        info.woodCount = getValueOrDefaultNone(objInfo, 'wood_cnt')

        return info


class PrivateApiInfoMapper(OpenApiInfoMapper):
    def __init__(self):
        super(PrivateApiInfoMapper, self).__init__()

    def mapObject(self, jsonData: str) -> PrivateApiInfo:
        openApiInfo: OpenApiInfo = super().mapObject(jsonData)

        privateApiInfo: PrivateApiInfo = PrivateApiInfo()
        privateApiInfo.__dict__.update(openApiInfo.__dict__)

        objInfo = json.loads(jsonData)
        privateApiInfo.health = getValueOrDefaultNone(objInfo, 'health')
        privateApiInfo.questProgress = getValueOrDefaultNone(objInfo, 'quest_progress')
        privateApiInfo.expProgress = getValueOrDefaultNone(objInfo, 'exp_progress')
        privateApiInfo.godPower = getValueOrDefaultNone(objInfo, 'godpower')
        privateApiInfo.diaryLast = getValueOrDefaultNone(objInfo, 'diary_last')
        # Город, в котором герой (пустая строка, если в поле, и нет ключа, если в бою)
        privateApiInfo.townName = getValueOrDefaultNone(objInfo, 'town_name')
        privateApiInfo.distance = getValueOrDefaultNone(objInfo, 'distance')
        privateApiInfo.arenaFight = getValueOrDefaultNone(objInfo, 'arena_fight')
        privateApiInfo.inventoryNum = getValueOrDefaultNone(objInfo, 'inventory_num')
        privateApiInfo.questName = getValueOrDefaultNone(objInfo, 'quest')
        privateApiInfo.activatables = getValueOrDefaultNone(objInfo, 'activatables')
        privateApiInfo.aura = getValueOrDefaultNone(objInfo, 'aura')
        privateApiInfo.expired = getValueOrDefaultNone(objInfo, 'expired')
        # TODO - сделать enum для данного значения
        privateApiInfo.fightType = getValueOrDefaultNone(objInfo, 'fight_type')
        # TODO - map pet
        privateApiInfo.pet = None

        return privateApiInfo