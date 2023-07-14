import pandas as pd
import pytest
from great_expectations.exceptions import GreatExpectationsError

from easy_ge.helpers import ValidationError
from easy_ge.main import easy_validation


def test_easy_validation_with_invalid_config():
    # Define an invalid configuration file path
    config_path = "tests/test_configs/invalid_config2.yaml"
    schema_path = "tests/test_configs/valid_schema.json"

    # Run the easy_validation function and expect it to raise an exception
    with pytest.raises(Exception):
        easy_validation(config_path)


def test_easy_validation_with_invalid_schema():
    # Define a valid configuration file path but invalid schema path
    config_path = "tests/test_configs/valid_config2.yaml"
    schema_path = "tests/test_configs/invalid_schema.json"

    # Run the easy_validation function and expect it to raise an exception
    with pytest.raises(Exception):
        easy_validation(config_path)

# def test_easy_validation_with_valid_config():
#     # Define a valid configuration file path
#     config_path = "tests/test_configs/valid_config2.yaml"
#     schema_path = "tests/test_configs/valid_schema.json"

#     # Run the easy_validation function
#     df = easy_validation(config_path)
#     print(df.columns)
#     # Assert that the returned DataFrame has the expected columns
#     assert set(df.columns) == set(["expectation_type", "success", "observed_value", "element_count", "missing_count", "missing_percent"])
