import json
from collections import namedtuple
from entity.entity import OpenApiInfo, PrivateApiInfo


# Преобразование json строки в объект python
def convertJsonToObject(jsonData: str) -> object:
    return json.loads(jsonData, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))


class OpenApiInfoMapper(object):
    def __init__(self):
        pass

    def mapObject(self, jsonData: str) -> OpenApiInfo:
        objInfo = convertJsonToObject(jsonData)
        info = OpenApiInfo()
        info.godName = objInfo.godname
        info.heroName = objInfo.name
        info.gender = objInfo.gender
        info.level = objInfo.level
        info.maxHealth = objInfo.max_health
        info.inventoryMaxNum = objInfo.inventory_max_num
        info.motto = objInfo.motto
        info.clan = objInfo.clan
        info.clanPosition = objInfo.clan_position
        info.alignment = objInfo.alignment
        info.bricksCnt = objInfo.bricks_cnt
        info.arkCompletedAt = objInfo.ark_completed_at
        info.arenaWonCount = objInfo.arena_won
        info.arenaLostCount = objInfo.arena_lost
        info.gold_approx = objInfo.gold_approx
        # TODO - что за X() в параметре?
        info.inventory = objInfo.inventory
        return info


class PrivateApiInfoMapper(object):
    def __init__(self):
        pass

    def mapObject(self, jsonData: str) -> PrivateApiInfo:
        # TODO дописать маппинг приватных параметров, при этом сделать
        # наследуемым текущий объект от другого
        pass