#!/usr/bin/env python
# -*- coding: utf-8; -*-

# Copyright (c) 2021, 2024 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/
from typing import Any, Dict

from ads.common.serializer import DataClassSerializable
from ads.ml_monitoring.application_config import ApplicationActionType
from ads.ml_monitoring.config_validator.validator_utils import validate_config


class ConfigValidator(DataClassSerializable):

    def validate_config(self, config : Dict[str, Any], action_type : str ):
        print("check if config is valid")
        result = validate_config(config=config, action_type=ApplicationActionType.from_string(action_type))
        print(result)