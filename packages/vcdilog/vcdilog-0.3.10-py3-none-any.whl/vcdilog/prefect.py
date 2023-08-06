import os
import pendulum
import vcdilog

from functools import partial
from typing import Dict, Union

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
    """
    Logger class for prefect flows which can be used to retreive and set common fields
    like flow_name, prefect tenant, prefect project, flow_run_id in prefect logs.

    PrefectLogger class can only be instantiated from a prefect task.

    Args:
        - batch_date: string representing flow parameter batch_date
                        defaults to 'batch-dt'
        - kwargs: any kwargs passed will be added to all logs defined
                    with PrefectLogger

    Raises:
        - ImportError: if prefect is not installed
        - RuntimeError: If this class is instantiated not from a prefect task
    """

    def __init__(
        self,
        batch_date: str = "batch-dt",
        **kwargs,
    ) -> None:

        try:
            import prefect
            from prefect.client.client import Client
        except ImportError as err:
            raise ImportError(
                "Using `PrefectLogger` requires prefect to be installed."
            ) from err

        self._prefect = prefect
        self._client = Client()

        try:
            # ensure we are in a prefect flow
            if "flow_name" not in prefect.context:
                raise NameError

            self._logger = vcdilog.get_prefect_logger()
            self._kwargs = self.__standardise_kwargs(**kwargs)
            flow = self.get_flow_details(batch_date)
            self._kwargs["tenant"] = flow["tenant"]
            self._kwargs["project"] = flow["project"]
            self._kwargs["flow-version"] = flow["flow-version"]
            self._kwargs["batch-date"] = flow["batch-date"]

        except NameError:
            raise RuntimeError("This must be executed within a prefect context")

    @staticmethod
    def __standardise_kwargs(**kwargs):
        return {k.replace("_", "-"): v for k, v in kwargs.items()}

    def get_flow_details(self, batch_date) -> dict:
        """
        Function to query Prefect GraphQL API to get flow related info that are not
        available in prefect context -
            * Tenant name
            * Project name
            * Flow version
            * Parameter: batch-date
        All fields defaults to "NA" if missing or in case of an error

        Args:
            - batch_date (string): string representing flow parameter batch_date
        Returns:
            - dict: dictionary with following keys-
                    tenant: str
                    project: str
                    flow-version: int
                    batch-date: str(date)

        """

        try:
            flow = {}
            query = """
                    query ($flow_run_id: uuid!){
                        flow_run (where: {id: {_eq: $flow_run_id}}){
                            tenant {
                                name
                            }
                            flow {
                                version
                                project {
                                    name
                                }
                            }
                            parameters
                        }
                    }
                    """
            variables = {"flow_run_id": self._prefect.context.flow_run_id}
            response = self._client.graphql(query=query, variables=variables)

            flow_run = response["data"]["flow_run"][0]
            flow["tenant"] = flow_run.get("tenant", {}).get("name", "NA")
            flow["project"] = flow_run.get("flow", {}).get("project", {}).get("name", "NA")
            flow["flow-version"] = flow_run.get("flow", {}).get("version", "NA")
            flow["batch-date"] = flow_run.get("parameters", {}).get(batch_date, "NA")
            return flow
        except Exception as e:
            log_level = get_logging_attr("WARNING")
            self._logger.log(log_level, "VCDILOG warning")
            self._logger.log(log_level, str(e))
            flow["tenant"] = flow["project"] = flow["batch-date"] = flow["flow-version"] = "NA"  # fmt: skip
            return flow

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
        tz = pendulum.timezone("Australia/Melbourne")
        _m = dict(
            {
                "msg-datetime": prefect.context.date.astimezone(tz).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                **self._kwargs,
                "flow-run-id": prefect.context.flow_run_id,
                "flow-name": prefect.context.flow_name,
                "flow-task": prefect.context.task_name,
                "source": kwargs.get("source", "NA"),
                "file": kwargs.get("file", "NA"),
                "status": kwargs.get("status", "NA"),
            },
        )

        _m.update({"msg": msg} if isinstance(msg, str) else msg)
        _m.update(self.__standardise_kwargs(**kwargs))

        self._logger.log(log_level, _m)

    def __getattr__(self, method):

        if method.startswith("_"):
            raise AttributeError

        return partial(self.log, log_level=method.upper())
