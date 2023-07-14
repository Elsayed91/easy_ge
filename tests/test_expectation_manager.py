# tests/test_expectation_manager.py

import sys
from unittest.mock import MagicMock, Mock, patch

import pandas as pd
import pytest
from easy_ge.expectation_manager import ExpectationManager
from great_expectations.data_context import BaseDataContext
from great_expectations.exceptions import GreatExpectationsError

sys.path.append('easy_ge')




@patch("easy_ge.expectation_manager.BaseDataContext")
@patch("easy_ge.helpers.TemplateHandler")
def test_prepare_data_context_2(mocked_template_handler_class, mocked_data_context_class):
    # Create a mock BaseDataContext instance
    mocked_data_context = MagicMock()
    mocked_data_context_class.return_value = mocked_data_context

    # Create a mock TemplateHandler instance
    mocked_template_handler = MagicMock()
    mocked_template_handler_class.return_value = mocked_template_handler

    # Initialize ExpectationManager
    expectation_manager = ExpectationManager(mocked_template_handler, mocked_template_handler, True)

    # Call the method to test
    expectation_manager.prepare_data_context({"Source": {"Name": "Test"}})

    # Check if the correct methods were called on the BaseDataContext instance
    mocked_template_handler.process_template.assert_called_once()
    mocked_data_context_class.assert_called_once()


@patch("easy_ge.expectation_manager.BaseDataContext")
@patch("easy_ge.helpers.TemplateHandler")
def test_prepare_checkpoint(mocked_template_handler_class, mocked_data_context_class):
    # Create a mock BaseDataContext instance
    mocked_data_context = MagicMock()
    mocked_data_context_class.return_value = mocked_data_context

    # Create a mock TemplateHandler instance
    mocked_template_handler = MagicMock()
    mocked_template_handler_class.return_value = mocked_template_handler

    # Initialize ExpectationManager
    expectation_manager = ExpectationManager(mocked_template_handler, mocked_template_handler, True)

    # Call the method to test
    expectation_manager.prepare_checkpoint({"Source": {"Name": "Test"}}, mocked_data_context)

    # Check if the correct methods were called
    mocked_template_handler.process_template.assert_called_once()
    mocked_data_context.add_checkpoint.assert_called_once()


@patch("easy_ge.expectation_manager.BaseDataContext")
@patch("easy_ge.helpers.TemplateHandler")
def test_run_checkpoint(mocked_template_handler_class, mocked_data_context_class):
    # Create a mock BaseDataContext instance
    mocked_data_context = MagicMock()
    mocked_data_context_class.return_value = mocked_data_context

    # Create a mock TemplateHandler instance
    mocked_template_handler = MagicMock()
    mocked_template_handler_class.return_value = mocked_template_handler

    # Initialize ExpectationManager
    expectation_manager = ExpectationManager(mocked_template_handler, mocked_template_handler, True)

    # Call the method to test
    expectation_manager.run_checkpoint({"Source": {"Name": "Test"}}, mocked_data_context)

    # Check if the correct methods were called
    mocked_data_context.run_checkpoint.assert_called_once()
    mocked_data_context.build_data_docs.assert_called_once()




@patch("easy_ge.expectation_manager.BaseDataContext")
@patch("easy_ge.helpers.TemplateHandler")
def test_prepare_checkpoint_calls_add_checkpoint(mocked_template_handler_class, mocked_data_context_class):
    # Create a mock BaseDataContext instance
    mocked_data_context = MagicMock()
    mocked_data_context_class.return_value = mocked_data_context

    # Create a mock TemplateHandler instance
    mocked_template_handler = MagicMock()
    mocked_template_handler_class.return_value = mocked_template_handler

    # Initialize ExpectationManager
    expectation_manager = ExpectationManager(mocked_template_handler, mocked_template_handler, True)

    # Define a valid configuration
    valid_config = "templates/valid_config.yaml"

    # Prepare a data context
    data_context = expectation_manager.prepare_data_context(valid_config)

    # Define a configuration
    config = {"some_key": "some_value"}

    # Prepare a checkpoint
    expectation_manager.prepare_checkpoint(config, data_context)

    # Assert that add_checkpoint was called with the correct arguments
    mocked_data_context.add_checkpoint.assert_called_once()

@patch("easy_ge.expectation_manager.BaseDataContext")
@patch("easy_ge.helpers.TemplateHandler")
def test_run_checkpoint_with_invalid_config(mocked_template_handler_class, mocked_data_context_class):
    # Create a mock BaseDataContext instance
    mocked_data_context = MagicMock()
    mocked_data_context_class.return_value = mocked_data_context

    # Create a mock TemplateHandler instance
    mocked_template_handler = MagicMock()
    mocked_template_handler_class.return_value = mocked_template_handler

    # Initialize ExpectationManager
    expectation_manager = ExpectationManager(mocked_template_handler, mocked_template_handler, True)

    # Define a valid configuration
    valid_config = "templates/valid_config.yaml"  # This should be a valid configuration for the data context

    # Prepare a data context
    data_context = expectation_manager.prepare_data_context(valid_config)

    # Define an invalid configuration
    config = {"Source": {"invalid_key": "invalid_value"}}

    # Run a checkpoint and expect it to raise an exception
    with pytest.raises(KeyError):
        expectation_manager.run_checkpoint(config, data_context)


def test_get_batch_request_parameters():
    # Create an instance of ExpectationManager
    expectation_manager = ExpectationManager(None, None, None)

    # Define a configuration
    config = {
        "Source": {
            "Properties": {
                "InMemory": {
                    "DataFrameName": "df"
                }
            }
        }
    }

    # Define a DataFrame
    df = pd.DataFrame()

    # Mock globals function to return df
    with patch("builtins.globals", return_value={"df": df}):
        # Call the method to test
        batch_type, batch_data = expectation_manager.get_batch_request_parameters(config)

        # Check if the output matches the expected output
        assert batch_type == "batch_data"
        assert isinstance(batch_data, pd.DataFrame)

