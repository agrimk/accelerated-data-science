#!/usr/bin/env python
# -*- coding: utf-8; -*-

# Copyright (c) 2021, 2024 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/
from typing import Any, Dict

from ads.common.serializer import DataClassSerializable
# from ads.ml_monitoring.application_config import ApplicationActionType
# from ads.ml_monitoring.config_validator.validator_utils import validate_config

import json

class ConfigAuthoring(DataClassSerializable):

    def add_to_schema(self, config_name:str, component_name:str, config_value : Dict[str, Any]):
        print("Generating config")
        config = {}
        with open(config_name, "w+") as file:
            config = json.load(file)
            config[component_name] = config_value
            print(config)
            file.write(json.dumps(config))

    def add_to_metrics(self, config_name: str, featureName: str, metric: Dict[str, Any]):
        print("Generating config")
        # config = {}
        # with open(config_name, "w+") as file:
        #     config = json.load(file)
        #     config[component_name] = config_value
        #     print(config)
        #     file.write(json.dumps(config))
