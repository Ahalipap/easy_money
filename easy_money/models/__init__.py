import datetime
import uuid
from abc import ABCMeta

from db import mongo

NoneType = type(None)


class BaseModel(metaclass=ABCMeta):
    database = 'easy_money'
    table = 'fund_companies'
    _db = mongo.mongo

    def __init__(self, uuid, **kwargs):
        self.uuid = uuid

    async def replace(self):
        return await self._db.replace_one(database=self.database, table_name=self.table, value=model2dict(self))


def model2dict(model):
    def _2dict(obj):
        rslt = {}
        for k, v in obj.__dict__.items():
            typev = type(v)
            if typev in (str, int, float, bool, datetime.datetime, uuid.UUID, NoneType):
                rslt[k] = v

            elif typev == list:
                if k.endswith('__list'):
                    rslt[k] = [_2dict(obj) for obj in v]
                else:
                    rslt[k] = [obj for obj in v if type(obj) in
                               (str, int, float, bool, dict, datetime.datetime, NoneType)]

            elif typev == dict:
                if k.endswith('__dict'):
                    rslt[k] = {_k: _2dict(_v) for _k, _v in v.items()}
                else:
                    rslt[k] = v  # CAUTION: v must be a primitive type
                    # raise Exception(f"the key '{k}' must be named as '{k}__dict'")

            elif isinstance(v, BaseModel):
                rslt[k] = _2dict(v)

        return rslt

    return _2dict(model)
