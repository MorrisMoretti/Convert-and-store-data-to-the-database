from enum import Enum


class RequestType(str, Enum):
    json = 'json'
    xml = 'xml'
