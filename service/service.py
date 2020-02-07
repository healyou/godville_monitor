from __future__ import annotations
import requests
import json
from entity.entity import OpenApiInfo, PrivateApiInfo
from mapper.mapper import OpenApiInfoMapper, PrivateApiInfoMapper


class GodvilleApiService(object):
    GODNAME_PARAM_KEY = '<godname>'
    TOKEN_PARAM_KEY = '<token>'

    GODVILLE_OPEN_API_URL = f'https://godville.net/gods/api/{GODNAME_PARAM_KEY}'
    GODVILLE_PRIVATE_API_URL = f'https://godville.net/gods/api/{GODNAME_PARAM_KEY}/{TOKEN_PARAM_KEY}'

    def get() -> GodvilleApiService:
        return GodvilleApiService()

    # Реализация одиночки
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GodvilleApiService, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        pass

    # Начитка открытой информации
    def loadOpenInfo(self, godname: str) -> OpenApiInfo:
        url = self.__configureOpenApiUrl(godname)
        answer = requests.get(url=url)
        data = answer.text
        mapper: OpenApiInfoMapper = OpenApiInfoMapper()
        return mapper.mapObject(data)

    # Начитка закрытой информации
    def loadPrivateInfo(self, godname: str, token: str) -> str:
        url = self.__configurePrivateApiUrl(godname, token)
        answer = requests.get(url=url)
        data = answer.text
        mapper: PrivateApiInfoMapper = PrivateApiInfoMapper()
        return mapper.mapObject(data)

    def __configureOpenApiUrl(self, godname: str) -> str:
        return self.GODVILLE_OPEN_API_URL.replace(self.GODNAME_PARAM_KEY, godname)

    def __configurePrivateApiUrl(self, godname: str, token: str) -> str:
        temp = self.GODVILLE_PRIVATE_API_URL.replace(self.GODNAME_PARAM_KEY, godname)
        return temp.replace(self.TOKEN_PARAM_KEY, token)