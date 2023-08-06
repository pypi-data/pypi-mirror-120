from typing import Any
import uuid
import json
import datetime
from collections.abc import Sequence

def dumper(obj: Any):
    if isinstance(obj, uuid.UUID):
        return str(obj)
    elif isinstance(obj, datetime.date):
        dat: datetime.date = obj
        return dat.isoformat()
    elif isinstance(obj, dict):
        return obj
    elif 'toJSON' in obj.__dict__:
        return obj.toJSON()
    else: 
        obj._owner = None # we remove _owner, because it causes circular reference error.
        d = obj.__dict__
        res: dict = {}
        for key in d:
            v = d[key]
            if v != None and \
                not (isinstance(v, Sequence) and len(v) == 0):
                res[key] = v
        return res

def toJSON(obj: Any) -> str:
    return json.dumps(obj, default=dumper, indent=2)
