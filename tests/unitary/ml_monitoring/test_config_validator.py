
import unittest
import pytest
import numpy as np
from unittest.mock import MagicMock, Mock, patch

from ads.common import auth as authutil
from ads.common import oci_client
from ads.ml_monitoring import ConfigValidator
from ads.model.deployment.model_deployment import (
    ModelDeployment,
    ModelDeploymentProperties,
)
from ads.model.deployment.model_deployment_infrastructure import ModelDeploymentInfrastructure
from ads.model.deployment.model_deployment_runtime import ModelDeploymentCondaRuntime


class ModelDeploymentTestCase(unittest.TestCase):
    MODEL_ID = "<MODEL_OCID>"
    with patch.object(oci_client, "OCIClientFactory"):
        config_validator = ConfigValidator()

    @patch("requests.post")
    # @patch("ads.model.deployment.model_deployment.ModelDeployment.sync")
    def test_config_validator(self, mock_sync, mock_post):
        """Ensures predict model passes with valid input parameters."""
        mock_sync.return_value = Mock(lifecycle_state="ACTIVE")
        mock_post.return_value = Mock(
            status_code=200, json=lambda: {"result": "result"}
        )
        with patch.object(authutil, "default_signer") as mock_auth:
            auth = MagicMock()
            auth["signer"] = MagicMock()
            mock_auth.return_value = auth
            test_result = self.config_validator.validate_config(config="test", action_type="RUN_BASELINE")
            # mock_post.assert_called_with(
            #     f"{self.config_validator.url}/predict",
            #     json="test",
            #     headers={"Content-Type": "application/json"},
            #     auth=mock_auth.return_value["signer"],
            # )
            # assert test_result == {"result": "result"}

        with pytest.raises(TypeError):
            self.config_validator.validate_config(action_type="RUN_BASELINE",config="test")
