# tests/test_expectation_manager.py

import sys
from unittest.mock import MagicMock, Mock, patch

import pandas as pd
import pytest
from easy_ge.expectation_manager import ExpectationManager
from easy_ge.helpers import TemplateHandler
from great_expectations.data_context import (AbstractDataContext,
                                             BaseDataContext)
from great_expectations.data_context.types.base import DataContextConfig
from great_expectations.exceptions import GreatExpectationsError

sys.path.append('easy_ge')




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
    mocked_data_context.add_or_update_checkpoint.assert_called_once()


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


        
        
class TestExpectationManager:

    # Tests that prepare_data_context raises an exception when given an invalid configuration
    def test_prepare_data_context_invalid_config(self, mocker):
        # Create a mock TemplateHandler instance
        mocked_template_handler = MagicMock()
        mocker.patch('easy_ge.helpers.TemplateHandler', return_value=mocked_template_handler)

        # Initialize ExpectationManager
        expectation_manager = ExpectationManager(mocked_template_handler, mocked_template_handler, True)

        # Define an invalid configuration
        invalid_config = {"invalid_key": "invalid_value"}

        # Call the method to test and expect it to raise an exception
        with pytest.raises(Exception):
            expectation_manager.prepare_data_context(invalid_config)

    # Tests that prepare_checkpoint adds or updates a checkpoint when given a valid configuration and data context
    def test_prepare_checkpoint_valid_config(self, mocker):
        # Create a mock BaseDataContext instance
        mocked_data_context = MagicMock()
        mocker.patch('easy_ge.expectation_manager.BaseDataContext', return_value=mocked_data_context)

        # Create a mock TemplateHandler instance
        mocked_template_handler = MagicMock()
        mocker.patch('easy_ge.helpers.TemplateHandler', return_value=mocked_template_handler)

        # Initialize ExpectationManager
        expectation_manager = ExpectationManager(mocked_template_handler, mocked_template_handler, True)

        # Define a valid configuration
        valid_config = {"Source": {"Name": "Test"}}

        # Call the method to test
        expectation_manager.prepare_checkpoint(valid_config, mocked_data_context)

        # Check if the correct methods were called
        mocked_template_handler.process_template.assert_called_once()
        mocked_data_context.add_or_update_checkpoint.assert_called_once()


            
    # Tests that run_checkpoint runs a checkpoint and returns a dictionary when given valid configuration and data context
    def test_run_checkpoint_valid_config(self, mocker):
        # Create a mock BaseDataContext instance
        mocked_data_context = MagicMock()
        mocker.patch('easy_ge.expectation_manager.BaseDataContext', return_value=mocked_data_context)

        # Create a mock TemplateHandler instance
        mocked_template_handler = MagicMock()
        mocker.patch('easy_ge.helpers.TemplateHandler', return_value=mocked_template_handler)

        # Initialize ExpectationManager
        expectation_manager = ExpectationManager(mocked_template_handler, mocked_template_handler, True)

        # Define a valid configuration
        valid_config = {"Source": {"Name": "Test"}}

        # Call the method to test
        expectation_manager.run_checkpoint(valid_config, mocked_data_context)

        # Check if the correct methods were called
        mocked_data_context.run_checkpoint.assert_called_once()
        mocked_data_context.build_data_docs.assert_called_once()


class TestPrepareDataContext:
    # Tests that passing a valid configuration dictionary returns an AbstractDataContext object.
    def test_valid_config(self):
        import os
        template_dir = os.path.abspath(os.path.dirname(__file__))  # Get the absolute path of the template directory
        great_expectations_tpl = os.path.join(template_dir, "../easy_ge/templates/great_expectations.tpl")
        checkpoint_tpl = os.path.join(template_dir, "../easy_ge/templates/checkpoint.tpl")

        self.expectation_manager = ExpectationManager(
            TemplateHandler(template_path=great_expectations_tpl),
            TemplateHandler(template_path=checkpoint_tpl),
            False
        )
        config = {
            "datasources": {
                "my_datasource": {
                    "data_asset_type": {
                        "class_name": "PandasDataset"
                    },
                    "module_name": "great_expectations.dataset",
                    "class_name": "PandasDatasource",
                    "path": "tests/test_data/sample_data.csv"
                }
            },
            "stores": {},
            "expectations_store_name": "expectations",
            "validations_store_name": "validations",
            "Source": {
                "Name": "my_datasource",
                "Properties": {
                    "File": {
                        "FilePath": "tests/test_data/sample_data.csv"
                    }
                }
            },
            "Backend": {
                "class_name": "TupleFilesystemBackend",
                "base_directory": "/tmp/great_expectations",
            }
        }
        result = self.expectation_manager.prepare_data_context(config)
        assert isinstance(result, AbstractDataContext)

    # Tests that passing an empty dictionary raises an Exception.
    def test_empty_config(self):
        with pytest.raises(Exception):
            self.expectation_manager.prepare_data_context({})

    # Tests that passing a non-dictionary object raises a TypeError.
    def test_non_dict_config(self):
        expectation_manager = ExpectationManager(None, None, False)
        with pytest.raises(TypeError):
            expectation_manager.prepare_data_context([])

    # Tests that an Exception is raised when the Great Expectations configuration is missing.
    def test_missing_config(self):
        with pytest.raises(Exception):
            self.expectation_manager.prepare_data_context(None)

    # Tests that the Great Expectations configuration is processed by the ge_template_handler.
    def test_processed_config(self):
        import os
        template_dir = os.path.abspath(os.path.dirname(__file__))  # Get the absolute path of the template directory
        great_expectations_tpl = os.path.join(template_dir, "../easy_ge/templates/great_expectations.tpl")
        checkpoint_tpl = os.path.join(template_dir, "../easy_ge/templates/checkpoint.tpl")

        self.expectation_manager = ExpectationManager(
            TemplateHandler(template_path=great_expectations_tpl),
            TemplateHandler(template_path=checkpoint_tpl),
            False
        )
        # Test that the Great Expectations configuration is processed by the ge_template_handler.
        config = {
            "datasources": {
                "my_datasource": {
                    "data_asset_type": {
                        "class_name": "PandasDataset"
                    },
                    "module_name": "great_expectations.dataset",
                    "class_name": "PandasDatasource",
                    "path": "tests/test_data/sample_data.csv"
                }
            },
            "stores": {},
            "expectations_store_name": "expectations_store",
            "validations_store_name": "validations_store",
            "Source": {
                "Name": "my_datasource",
                "Type": "PandasDatasource",
                "Properties": {
                    "File": {
                        "FilePath": "tests/test_data/sample_data.csv"
                    }
                }
            },
            "Backend": {
                "class_name": "TupleFilesystemBackend",
                "base_directory": "/tmp/great_expectations",
            }
        }
        result = self.expectation_manager.prepare_data_context(config)
        expected_output = {
            "datasources": {
                "my_datasource": {
                    "module_name": "great_expectations.datasource",
                    "class_name": "Datasource",
                    "execution_engine": {
                        "module_name": "great_expectations.execution_engine",
                        "class_name": "ExecutionEngine"
                    },
                    "data_connectors": {
                        "default_runtime_data_connector_name": {
                            "class_name": "RuntimeDataConnector",
                            "batch_identifiers": ["default_identifier_name"]
                        }
                    }
                }
            },
            "expectations_store_name": "expectations_store",
            "validations_store_name": "validations_store",
            "stores": {},
            "config_version": 3,
            "config_variables_file_path": None,
            "plugins_directory": None,
            "plugins": {},
            "validation_operators": {},
            "data_docs_sites": {
                "my_datasourceDocs": {
                    "class_name": "SiteBuilder",
                    "site_index_builder": {
                        "class_name": "DefaultSiteIndexBuilder"
                    }
                }
            },
            "anonymous_usage_statistics": {
                "usage_statistics_url": "https://stats.greatexpectations.io/great_expectations/v1/usage_statistics",
                "explicit_id": True,
                "explicit_url": False,
                "data_context_id": result._project_config['anonymous_usage_statistics']['data_context_id'],
                "enabled": True
            },
            "notebooks": {},
            "data_docs": {},
            "checkpoint_store_name": result._project_config['checkpoint_store_name'],
            "validation_store_name": None,
            "project_name": None,
            "config_variables": {},
            "fluent_datasources": {},
            "include_rendered_content": {
                "globally": False,
                "expectation_validation_result": False,
                "expectation_suite": False
            },
            "evaluation_parameter_store_name": "evaluation_parameter_store",
            "data_docs_sites": {
                "my_datasourceDocs": {
                    "class_name": "SiteBuilder",
                    "site_index_builder": {
                        "class_name": "DefaultSiteIndexBuilder"
                    },
                    "store_backend": None
                }
            }
        }
        assert result._project_config["datasources"] == expected_output["datasources"]
        assert result._project_config["expectations_store_name"] == expected_output["expectations_store_name"]
        assert result._project_config["validations_store_name"] == expected_output["validations_store_name"]
        assert result._project_config["data_docs_sites"]["my_datasourceDocs"]["class_name"] == expected_output["data_docs_sites"]["my_datasourceDocs"]["class_name"]
        assert result._project_config["data_docs_sites"]["my_datasourceDocs"]["site_index_builder"] == expected_output["data_docs_sites"]["my_datasourceDocs"]["site_index_builder"]        
        assert result._project_config["checkpoint_store_name"] == expected_output["checkpoint_store_name"]
        assert result._project_config["evaluation_parameter_store_name"] == expected_output["evaluation_parameter_store_name"]
