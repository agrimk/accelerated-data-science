from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict
# from application.exceptions.application_exception import InvalidConfigException


class ApplicationActionType(Enum):
    RUN_BASELINE = 1
    RUN_PREDICTION = 2
    RUN_CONFIG_VALIDATION = 3

    @staticmethod
    def from_string(action_type: str) -> 'ApplicationActionType':
        try:
            return ApplicationActionType[action_type.upper()]
        except KeyError:
            print("invalid config")
            # raise InvalidConfigException(config_source=ApplicationActionType.__name__,
            #                              error_message=f"{action_type} is not a valid member of ApplicationActionType")


@dataclass
class RuntimeParameter:
    action_type: str
    date_range: Dict[str, Any]

    def __init__(self, ACTION_TYPE: str = '',
                 DATE_RANGE: Dict[str, Any] = None) -> None:  # type: ignore
        super().__init__()
        self.action_type = ACTION_TYPE
        self.date_range = DATE_RANGE


@dataclass
class ApplicationConfig:
    config_location: str
    runtime_parameter: RuntimeParameter

    def __init__(self, config_location: str, runtime_parameter: RuntimeParameter) -> None:
        super().__init__()
        self.config_location = config_location
        self.runtime_parameter = runtime_parameter


