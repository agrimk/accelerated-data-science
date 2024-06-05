#!/usr/bin/env python
# -*- coding: utf-8; -*-

# Copyright (c) 2021, 2023 Oracle and/or its affiliates.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl/


import logging

logger = logging.getLogger(__name__)
try:
    from ads.ml_monitoring.config_validator.config_validator import ConfigValidator
    from ads.ml_monitoring.config_authoring.config_authoring import ConfigAuthoring
except AttributeError as e:
    import oci.data_science

    if not hasattr(oci.data_science.models, "Job"):
        logger.warning(
            "The OCI SDK you installed does not support Data Science ML Monitoring. ADS ML Monitoring API will not work."
        )
    else:
        raise e

__all__ = [
    "ConfigValidator",
    "ConfigAuthoring"
]
