import json
from typing import List, Dict
from entity.entity import OpenApiInfo, PrivateApiInfo
from logic.notification_items import NotificationItem


class OpenApiInfoMapper(object):
    def __init__(self):
        pass

    def mapObject(self, jsonData: str) -> OpenApiInfo:
        objInfo = json.loads(jsonData)

        info = OpenApiInfo()

        for item in NotificationItem:
            if (item.isOpenInfo):
                propName: str = item.propertyName
                jsonPropName: str = item.jsonPropName
                mapper = item.mapper
                value = mapper.mapObject(objInfo, jsonPropName)
                setattr(info, propName, value)

        return info


class PrivateApiInfoMapper(OpenApiInfoMapper):
    def __init__(self):
        super(PrivateApiInfoMapper, self).__init__()

    def mapObject(self, jsonData: str) -> PrivateApiInfo:
        openApiInfo: OpenApiInfo = super().mapObject(jsonData)

        privateApiInfo: PrivateApiInfo = PrivateApiInfo()
        privateApiInfo.__dict__.update(openApiInfo.__dict__)
        objInfo = json.loads(jsonData)

        for item in NotificationItem:
            if (not item.isOpenInfo):
                propName: str = item.propertyName
                jsonPropName: str = item.jsonPropName
                mapper = item.mapper
                value = mapper.mapObject(objInfo, jsonPropName)
                setattr(privateApiInfo, propName, value)

        return privateApiInfo
