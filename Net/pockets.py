import json

class HandShake():
    def __init__(self, id):
        self.header = "HANDSHAKE"
        self.id = id

class UserConnection():
    def __init__(self, code, money, winchance):
        self.header = "USER_CONNECTION"
        self.data = {
            "code": code,
            "money": money,
            "winchance": winchance
        }

    def to_json(self):
        return json.dumps(self.__dict__)
    
    def to_bytearray(self):
        json_str = self.to_json()
        json_bytes = json_str.encode('utf-8')
        return bytearray(json_bytes)
    
class UserResult:
    def __init__(self, code: int, start: int, end: int):
        self.header = 'USER_RESULT'
        self.code = code
        self.start = start
        self.end = end

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls(
            code=data['code'],
            start=data['start'],
            end=data['end']
        )

    def to_json(self) -> str:
        return json.dumps({
            'header': self.header,
            'code': self.code,
            'start': self.start,
            'end': self.end
        })