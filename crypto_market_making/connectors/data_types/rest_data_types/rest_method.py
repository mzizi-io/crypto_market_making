from enum import Enum

class RESTMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

    def __str__(self):
        obj_str = repr(self)
        return obj_str

    def __repr__(self):
        return self.value
