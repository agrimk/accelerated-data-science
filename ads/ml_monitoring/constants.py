from enum import Enum
from typing import TypeVar, Type, List, Union

from ads.ml_monitoring.application_config import ApplicationActionType

CONFIG_LOCATION = 'CONFIG_LOCATION'
RUNTIME_PARAMETER_KEY = 'RUNTIME_PARAMETER'
APPLICATION_DATE_RANGE_KEY = 'DATE_RANGE'
APPLICATION_ACTION_TYPE_KEY = 'ACTION_TYPE'

BASELINE_FOLDER = 'baseline'
PREDICTION_FOLDER = 'prediction'

APPLICATION_PREFIX = 'mlm'
FILE_PATH = 'file_path'
PAYLOAD = 'payload'
PAYLOAD_TYPE = 'payload_type'
OCI_PROFILE_FOLDER_NAME = 'profile'
OCI_PROFILE_FILE_NAME = 'profile.bin'
OCI_APPLICATION_CONFIG_FOLDER_NAME = 'application_config'
OCI_APPLICATION_CONFIG_FILE_NAME = 'application_config.json'

OCI_PAYLOAD_PATH_FORMAT = '%Y/%m/%d'
OCI_FILE_PATH_FORMAT = 'oci://%s@%s/%s'

BASELINE_READER = 'baseline_reader'
PREDICTION_READER = 'prediction_reader'
READER_KEY = 'reader'
START = 'start'
END = 'end'
POST_PROCESSOR_KEY = 'post_processors'
TRANSFORMERS_KEY = 'transformers'
TYPE = 'type'
PARAMS = 'params'
DATE_RANGE = 'date_range'
DATA_SOURCE = 'data_source'
FILTER_ARG = 'filter_arg'
OBJECT_STORAGE_FILE_SEARCH_DATA_SOURCE = 'ObjectStorageFileSearchDataSource'
PARTITION_BASED_DATE_RANGE = 'partition_based_date_range'
SAVE_METRIC_OUTPUT_AS_JSON_WRITER_POST_PROCESSOR = 'SaveMetricOutputAsJsonPostProcessor'
INPUT_SCHEMA = 'input_schema'
FEATURE_METRICS = 'feature_metrics'
DATASET_METRICS = 'dataset_metrics'
TAGS = 'tags'
MONITOR_ID = 'monitor_id'
MONITOR_RUN_ID = 'monitor_run_id'
ENGINE_DETAIL = 'engine_detail'
ENGINE_NAME = 'engine_name'
DASK = 'dask'

PROFILE_JSON = 'profile.json'
START_PLACEHOLDER = '$start'
END_PLACEHOLDER = '$end'
ACTION_TYPE_PLACEHOLDER = '$action_type'
MONITOR_ID_PLACEHOLDER = '$monitor_id'
REPLACEMENT_LOCATION_PLACEHOLDER = '$location'
DEFAULT_FILE_LOCATION_EXPRESSION = '$location/$monitor_id/$action_type/'
DEFAULT_FILE_LOCATION_EXPRESSION_WITH_DATE_RANGE = '$location/$monitor_id/$action_type/$start-$end/'
LOCATION = 'location'
UNDERSCORE_DELIMITER = '_'
JSON_FILE_TYPE = '.json'

STORAGE_DETAILS = 'storage_details'
STORAGE_TYPE = 'storage_type'
NAMESPACE = "namespace"
BUCKET_NAME = "bucket_name"
OBJECT_PREFIX = "object_prefix"
OCI_OBJECT_STORAGE = "OciObjectStorage"


class AbstractEnum:
    @classmethod
    def supported_names(cls, enum_type: Type[Enum]) -> List[object]:
        return [member.name for member in enum_type]

    @classmethod
    def supported_values(cls, enum_type: Type[Enum]) -> List[object]:
        return [member.value for member in enum_type]

    @classmethod
    def has_name(cls, enum_type: Type[Enum], name: object) -> bool:
        return name in cls.supported_names(enum_type=enum_type)

    @classmethod
    def has_value(cls, enum_type: Type[Enum], value: object) -> bool:
        return value in cls.supported_values(enum_type=enum_type)


class PayloadType(Enum):
    BYTES = bytes
    STRING = str


Payload = TypeVar("Payload", bound=Union[bytes, str])


def get_evaluation_folder(action_type: ApplicationActionType) -> str:
    if not action_type:
        raise ValueError("Action type not provided, provide from [%s]" % AbstractEnum.supported_names(
            enum_type=ApplicationActionType))
    return BASELINE_FOLDER if action_type == ApplicationActionType.RUN_BASELINE else PREDICTION_FOLDER
