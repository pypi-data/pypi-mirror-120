import os
import pytz
from functools import partial
from typing import Dict, Union

import vcdilog

from .obj import get_logging_attr


def get_prefect_logger(name: str = "logger"):
    try:
        import prefect
    except ImportError as err:
        raise ImportError(
            "Using `get_prefect_logger` requires prefect to be installed."
        ) from err

    return prefect.context.get(name)


def set_prefect_extra_loggers(loggers_list):
    formatted = repr(loggers_list)

    VAR = "PREFECT__LOGGING__EXTRA_LOGGERS"
    os.environ[VAR] = formatted


class PrefectLogger:
    def __init__(
        self, pipeline_stage: str = "NA", batch_date: str = "NA", **kwargs
    ) -> None:

        try:
            import prefect
        except ImportError as err:
            raise ImportError(
                "Using `PrefectLogger` requires prefect to be installed."
            ) from err

        self._prefect = prefect

        try:
            # ensure we are in a prefect flow
            if "flow_name" not in prefect.context:
                raise NameError

            self._logger = vcdilog.get_prefect_logger()
            self._kwargs = self.__standardise_kwargs(**kwargs)
            self._kwargs["pipeline-stage"] = pipeline_stage
            self._kwargs["batch-date"] = batch_date

        except NameError:
            raise RuntimeError("This must be executed within a prefect context")

    @staticmethod
    def __standardise_kwargs(**kwargs):
        return {k.replace("_", "-"): v for k, v in kwargs.items()}

    def log(
        self,
        msg: Union[str, Dict[str, str]],
        log_level: Union[int, str],
        **kwargs,
    ) -> None:

        log_level = log_level or "INFO"

        if isinstance(log_level, str):
            log_level = get_logging_attr(log_level)

        prefect = self._prefect
        _m = {
            "msg-datetime": prefect.context.date.astimezone(
                pytz.timezone("Australia/Melbourne")
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "flow-name": prefect.context.flow_name,
            "flow-task": prefect.context.task_name,
            "flow-run-id": prefect.context.flow_run_id,
            "source": kwargs.get("source", "NA"),
            "file": kwargs.get("file", "NA"),
            "status": kwargs.get("status", "NA"),
        }

        _m.update({"msg": msg} if isinstance(msg, str) else msg)
        _m.update(self.__standardise_kwargs(**kwargs))

        self._logger.log(log_level, _m)

    def __getattr__(self, method):

        if method.startswith("_"):
            raise AttributeError

        return partial(self.log, log_level=method.upper())
