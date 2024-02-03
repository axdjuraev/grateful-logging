import json
import logging
from typing import TypeAlias


TDefaultKey: TypeAlias = str 
TAlisKey: TypeAlias = str


class JSONFormatter(logging.Formatter):
    def __init__(self, include_keys: "dict[TDefaultKey, TAlisKey]"):
        super().__init__()

        if not include_keys.keys():
            raise ValueError("include_fields cannot be None")
        
        self._include_fields = include_keys 

    def format(self, record: "logging.LogRecord") -> str:
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: "logging.LogRecord"):
        message = {
            alias: record.__dict__[key] 
            for key, alias in self._include_fields.items()
        }

        return message
