import pytest
from easy_ge.helpers import ConfigLoader, ValidationError


def test_load_config():
    # Test valid config
    config_path = "tests/test_configs/valid_config.yaml"
    schema_path = "schema.json"
    config_loader = ConfigLoader(config_path, schema_path)
    try:
        config = config_loader.load_config()
        assert isinstance(config, dict)
    except ValidationError:
        pytest.fail("ValidationError was raised with valid config.")

    # Test invalid config
    config_path = "tests/test_configs/invalid_config.yaml"
    config_loader = ConfigLoader(config_path, schema_path)
    with pytest.raises(ValidationError):
        config_loader.load_config()
