import importlib
import re
from typing import Dict, Any, List

from dateutil.parser import ParserError, parse  # type:ignore
from mlm_insights.config_reader.utils.config_registry import ConfigRegistry  # type:ignore
import mlm_insights.utils.config_validator_util.config_validator_utils as ConfigValidatorUtils  # type:ignore

import json

from mlm_insights.config_reader.utils.config_registry import ConfigRegistry

from ads.ml_monitoring.application_config import ApplicationActionType, RuntimeParameter
from ads.ml_monitoring.constants import MONITOR_ID, BASELINE_READER, PREDICTION_READER, READER_KEY, \
    SAVE_METRIC_OUTPUT_AS_JSON_WRITER_POST_PROCESSOR, STORAGE_TYPE, STORAGE_DETAILS, NAMESPACE, OCI_OBJECT_STORAGE, PARAMS, BUCKET_NAME,START, DATE_RANGE, \
    END, APPLICATION_ACTION_TYPE_KEY



def validate_config(config: Dict[str, Any], action_type: ApplicationActionType) -> Dict[str, Any]:
    print("Starting application config grammar and component validation")
    error_list: Dict[str, Any] = {}
    config_registry = ConfigRegistry()

    # register dask components as engine is dask
    config_registry.add_dask_components()

    print("validating application components.")
    validate_application_components(config, error_list, action_type, config_registry.get_config_map())
    print("validating library components.")
    validate_library_components(config, error_list, config_registry.get_config_map())
    if error_list:
        print("Validation failed!")
        print(json.dumps(error_list, indent=4))
        # raise ConfigValidationException(error_list)

    print("Application config grammar and component validation is successful.")
    return error_list



def validate_library_components(config: Dict[str, Any], error_list: Dict[str, Any], config_map: Dict[str, Any]) -> None:
    # validate input schema
    print("validating library component - input schema.")
    input_schema, schema_errors = ConfigValidatorUtils.generate_input_schema(config)
    error_list.update(schema_errors)

    # validate data set metrics
    print("validating library component - dataset metrics.")
    data_set_metrics, data_set_metrics_errors, warning_dict_dm = ConfigValidatorUtils. \
        get_data_set_metrics(config, config_map, [])
    error_list.update(data_set_metrics_errors)

    # validate feature set metrics
    print("validating library component - feature set metrics.")
    feature_metrics, feature_metrics_error, warning_dict_fm = ConfigValidatorUtils. \
        get_univariate_metrics(config, config_map, [])
    error_list.update(feature_metrics_error)

    # validate transformers
    print("validating library component - transformers.")
    transformers, transformers_error, warning_dict_transformers = ConfigValidatorUtils. \
        get_transformers(config, config_map, [])
    error_list.update(transformers_error)

    # validate post processor
    print("validating library component - post processor.")
    save_metric_output_as_json_post_processor = getattr(importlib.import_module(
        'application.post_processors.save_metric_output_as_json_post_processor'),
        'SaveMetricOutputAsJsonPostProcessor')
    config_map[SAVE_METRIC_OUTPUT_AS_JSON_WRITER_POST_PROCESSOR] = save_metric_output_as_json_post_processor

    post_processor, post_processor_errors, warning_dict_pp = ConfigValidatorUtils. \
        get_post_processors(config, config_map, [])
    error_list.update(post_processor_errors)


def validate_application_components(config: Dict[str, Any], error_list: Dict[str, Any],
                                    action_type: ApplicationActionType, config_map: Dict[str, Any]) -> None:
    print("validating application component - monitor_id.")
    validate_monitor_id(config, error_list)
    print("validating application component - storage_details.")
    validate_storage_details(config, error_list)
    print("validating application component - readers.")
    validate_readers(config, error_list, action_type, config_map)


def validate_monitor_id(config: Dict[str, Any], error_list: Dict[str, Any]) -> None:
    if MONITOR_ID in config:
        if not is_monitor_id_valid(config[MONITOR_ID]):
            error_list[MONITOR_ID] = "monitor_id passed is in incorrect format. The length should be minimum 8 " \
                                     "characters and maximum 48 characters. Valid characters are letters (upper or " \
                                     "lowercase), numbers, hyphens, underscores, and periods. "
    else:
        print("monitor_id not present in the config.")
        error_list[MONITOR_ID] = "monitor_id is a required component. " \
                                 "Provide an monitor_id in the config."


def is_monitor_id_valid(monitor_id: str) -> bool:
    pattern = r'^[a-zA-Z0-9\-_\.]{8,48}$'
    if re.match(pattern, monitor_id):
        return True
    else:
        return False


def validate_readers(config: Dict[str, Any], error_list: Dict[str, Any],
                     action_type: ApplicationActionType, config_map: Dict[str, Any]) -> Any:
    if action_type == ApplicationActionType.RUN_BASELINE:
        validate_application_reader(config, error_list, config_map, BASELINE_READER)

    elif action_type == ApplicationActionType.RUN_PREDICTION:
        validate_application_reader(config, error_list, config_map, PREDICTION_READER)

    elif action_type == ApplicationActionType.RUN_CONFIG_VALIDATION:
        if BASELINE_READER not in config and PREDICTION_READER not in config:
            error_list[READER_KEY] = "Provide a reader component [baseline_reader and/or prediction_reader] in the " \
                                     "config."
        else:
            if BASELINE_READER in config:
                validate_application_reader(config, error_list, config_map, BASELINE_READER)
            if PREDICTION_READER in config:
                validate_application_reader(config, error_list, config_map, PREDICTION_READER)


def validate_application_reader(config: Dict[str, Any], error_list: Dict[str, Any],
                                config_map: Dict[str, Any], reader_type: str) -> Any:
    print("Validating: {}".format(reader_type))
    reader = None
    if reader_type in config:
        reader_value = config[reader_type]
        reader_dict = {READER_KEY: reader_value}
        reader, reader_error, warning_dict = ConfigValidatorUtils. \
            get_reader(reader_dict, config_map, [])
        if bool(reader_error):
            print("Provided an invalid {} component in the config.".format(reader_type))
            error_list[reader_type] = "Provided an invalid component. Provide a valid {}.".format(reader_type)
    else:
        print("Provide a {} component in the config.".format(reader_type))
        error_list[reader_type] = "{} is a required component." \
                                  "Provide a {} component in the config.".format(reader_type,
                                                                                 reader_type)
    return reader


# DATE_RANGE RUN_TIME PARAM Validation
# Check whether syntax of date_time ,
# Check whether both start and end is passed
# Check whether the start and end is valid date or some random string
# Check whether end is equal or more than start
# Check whether format of both start and end matches
def validate_date_range_runtime_param(date_range: Dict[str, Any]) -> None:
    date_range_keys = date_range.keys()
    if START not in date_range_keys or END not in date_range_keys or len(date_range) != 2:
        print("The value for required parameter in DATE_RANGE is invalid")
        # raise InvalidConfigException(config_source=DATE_RANGE,
        #                              error_message=str("The value for required parameter in DATE_RANGE is invalid"))

    try:
        parse(date_range[START])
    except ParserError as exception_message:
        print(str("The value for start parameter for DATE_RANGE is invalid"))

        # raise InvalidConfigException(config_source=DATE_RANGE,
        #                              error_message=str("The value for start parameter for DATE_RANGE is invalid"),
        #                              throwable=exception_message)

    try:
        parse(date_range[END])
    except ParserError as exception_message:
        print("The value for end parameter for DATE_RANGE is invalid")
        # raise InvalidConfigException(config_source=DATE_RANGE,
        #                              error_message=str("The value for end parameter for DATE_RANGE is invalid"),
        #                              throwable=exception_message)

    start = parse(date_range[START])
    end = parse(date_range[END])
    if end < start:
        print("The value/format of start and end parameter for DATE_RANGE is invalid")
        # raise InvalidConfigException(config_source=DATE_RANGE,
        #                              error_message=str(
        #                                  "The value/format of start and end parameter for DATE_RANGE is invalid"))


def validate_runtime_parameters(runtime_parameter_obj: RuntimeParameter) -> None:
    if runtime_parameter_obj and runtime_parameter_obj.action_type:
        action_type: str = runtime_parameter_obj.action_type
        ApplicationActionType.from_string(action_type)

    else:
        print("The Value for required parameter ACTION_TYPE is empty ")
        # raise InvalidConfigException(config_source=APPLICATION_ACTION_TYPE_KEY,
        #                              error_message=str("The Value for required parameter ACTION_TYPE is empty "))
    if runtime_parameter_obj.date_range:
        validate_date_range_runtime_param(runtime_parameter_obj.date_range)


def validate_storage_details(config: Dict[str, Any], error_list: Dict[str, Any]) -> None:
    if STORAGE_DETAILS in config.keys():
        storage_details_dict = config[STORAGE_DETAILS]
        if STORAGE_TYPE in storage_details_dict.keys():
            if storage_details_dict[STORAGE_TYPE] == OCI_OBJECT_STORAGE:
                required_param = [NAMESPACE, BUCKET_NAME]
                check_required_param(storage_details_dict, required_param, error_list)
            else:
                print("Provide a valid storage_type in storage_details component in the config. Supported Type"
                             " - OciObjectStorage.")
                error_list[STORAGE_DETAILS] = "Provide a valid storage_type in storage_details component " \
                                              "in the config. Supported Type - OciObjectStorage."
        else:
            print("Provide a storage_type in storage_details component in the config.")
            error_list[STORAGE_DETAILS] = "Provide a storage_type in storage_details component in the config."
    else:
        print("Provide a storage_details component in the config.")
        error_list[STORAGE_DETAILS] = "storage_details is a required component." \
                                      "Provide a storage_details component in the config."


def check_required_param(storage_details_dict: Dict[str, Any], required_param: List[str], error_list: Dict[str, Any]) \
        -> None:
    if "params" in storage_details_dict.keys():
        for param in required_param:
            if param not in storage_details_dict[PARAMS].keys():
                print("Provide the required param {} for storage_details component in the config.".format(param))
                error_list[
                    STORAGE_DETAILS + " " + param] = "Provide the required param {} for storage_details component in " \
                                                     "the config.".format(param)
    else:
        print("Provide the required params for storage_details component in the config.")
        error_list[STORAGE_DETAILS] = "Provide the required params for storage_details component in the " \
                                      "config."
