import json
from enum import Enum
from typing import List, Dict


class DNSRecord:
    def __init__(self, type, name, content):
        self.type = type
        self.name = name
        self.content = content

    def to_json(self) -> Dict:
        return {k: v.name if isinstance(v, Enum) else v for k, v in self.__dict__.items()}

    @classmethod
    def from_json(cls, json_str) -> 'DNSRecord':
        data = json.loads(json_str)
        return cls(**data)

    @classmethod
    def from_json_list(cls, json_list_str) -> List['DNSRecord']:
        data_list = json.loads(json_list_str)
        return [cls(**data) for data in data_list]

    @classmethod
    def to_json_list(cls, records) -> List[Dict]:
        return [record.to_json() for record in records]
