import enum


class RequestTypes(enum.Enum):
    GET = enum.auto()
    POST = enum.auto()
    PUT = enum.auto()
    DELETE = enum.auto()
    PATCH = enum.auto()


GET = RequestTypes.GET.name
POST = RequestTypes.POST.name
PUT = RequestTypes.PUT.name
DELETE = RequestTypes.DELETE.name
PATCH = RequestTypes.PATCH.name
