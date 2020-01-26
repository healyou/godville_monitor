from service.service import GodvilleApiService
from entity.entity import OpenApiInfo, PrivateApiInfo


service = GodvilleApiService()
openApiInfo: OpenApiInfo = service.loadOpenInfo('God name')
print(openApiInfo.__dict__)

privateApiInfo: PrivateApiInfo = service.loadPrivateInfo('God name', 'key')
print(privateApiInfo.__dict__)