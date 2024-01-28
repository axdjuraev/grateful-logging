import json
import logging
import datetime as dt
from typing_extensions import override


class JSONFormatter(logging.Formatter):
    LOG_RECORD_EXTRA_KEYS = ["extra"]

    def __init__(
        self,
        *,
        fmt_keys: "dict[str, str] | None" = None,
    ):
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    @override
    def format(self, record: "logging.LogRecord") -> str:
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: "logging.LogRecord"):
        always_fields = {
            "message": record.getMessage(),
            "timestamp": (dt.datetime.fromtimestamp(record.created).isoformat()),
        }

        if record.exc_info is not None:
            always_fields["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            always_fields["stack_info"] = self.formatStack(record.stack_info)

        message = {
            key: msg_val
            if (msg_val := always_fields.get(val, None)) is not None
            else getattr(record, val)
            for key, val in self.fmt_keys.items()
        }
        message.update(always_fields)

        for key, val in record.__dict__.items():
            if key in self.LOG_RECORD_EXTRA_KEYS:
                message[key] = val

        return message