from service.service import GodvilleApiService
from entity.entity import OpenApiInfo, PrivateApiInfo


service = GodvilleApiService()
openApiInfo: OpenApiInfo = service.loadOpenInfo('God Name')
print(openApiInfo.__dict__)