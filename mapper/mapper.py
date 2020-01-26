import json
from typing import List, Dict
from collections import namedtuple
from entity.entity import OpenApiInfo, PrivateApiInfo


def convertDictKeysToList(dict: Dict) -> List:
    items: List = list()
    for key, value in dict.keys():
        items.append(key)
    return items


class OpenApiInfoMapper(object):
    def __init__(self):
        pass

    def mapObject(self, jsonData: str) -> OpenApiInfo:
        objInfo = json.loads(jsonData)

        info = OpenApiInfo()
        info.godName = objInfo['godname']
        info.heroName = objInfo['name']
        info.gender = objInfo['gender']
        info.level = objInfo['level']
        info.maxHealth = objInfo['max_health']
        info.inventoryMaxNum = objInfo['inventory_max_num']
        info.motto = objInfo['motto']
        info.clan = objInfo['clan']
        info.clanPosition = objInfo['clan_position']
        info.alignment = objInfo['alignment']
        info.bricksCnt = objInfo['bricks_cnt']
        info.arkCompletedAt = objInfo['ark_completed_at']
        info.arenaWonCount = objInfo['arena_won']
        info.arenaLostCount = objInfo['arena_lost']
        info.gold_approx = objInfo['gold_approx']
        # Приходит список, а в python воспринимается как словарь
        info.inventory = convertDictKeysToList(objInfo.get('inventory', dict()))
        
        return info


class PrivateApiInfoMapper(OpenApiInfoMapper):
    def __init__(self):
        super(PrivateApiInfoMapper, self).__init__()

    def mapObject(self, jsonData: str) -> PrivateApiInfo:
        openApiInfo: OpenApiInfo = super().mapObject(jsonData)

        privateApiInfo: PrivateApiInfo = PrivateApiInfo()
        privateApiInfo.__dict__.update(openApiInfo.__dict__)

        objInfo = json.loads(jsonData)
        privateApiInfo.health = objInfo['health']
        privateApiInfo.questProgress = objInfo['quest_progress']
        privateApiInfo.expProgress = objInfo['exp_progress']
        privateApiInfo.godPower = objInfo['godpower']
        privateApiInfo.diaryLast = objInfo['diary_last']
        # Город, в котором герой (пустая строка, если в поле, и нет ключа, если в бою)
        privateApiInfo.townName = objInfo.get('town_name', None)
        privateApiInfo.distance = objInfo['distance']
        privateApiInfo.arenaFight = objInfo['arena_fight']
        privateApiInfo.inventoryNum = objInfo['inventory_num']
        privateApiInfo.questName = objInfo['quest']
        privateApiInfo.activatables = objInfo['activatables']

        return privateApiInfo