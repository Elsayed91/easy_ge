# great_expectations_wrapper/expectation_manager.py

"""
This module contains a class for managing Great Expectations operations.
"""

from typing import Any, Optional

import pandas as pd
from great_expectations.data_context import (AbstractDataContext,
                                             BaseDataContext)
from great_expectations.data_context.types.base import DataContextConfig

try:
    from easy_ge.helpers import TemplateHandler
except:
    from helpers import TemplateHandler

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logging.getLogger('great_expectations.data_context.data_context.abstract_data_context').setLevel(logging.WARNING)

class ExpectationManager:
    """
    A class for managing Great Expectations operations.
    """

    def __init__(self, ge_template_handler: TemplateHandler, cp_template_handler: TemplateHandler, generate_docs: bool):
        self.ge_template_handler = ge_template_handler
        self.cp_template_handler = cp_template_handler
        self.generate_docs = generate_docs

    def prepare_data_context(self, config: dict[str, Any]) -> AbstractDataContext:
        """
        Prepare a data context from the Great Expectations configuration.

        Args:
            config: The Great Expectations configuration.

        Returns:
            A BaseDataContext object.
        """
        logging.info("Preparing data context...")
        ge_config = self.ge_template_handler.process_template(config)
        return BaseDataContext(DataContextConfig(**ge_config))

    def prepare_checkpoint(self, config: dict[str, Any], data_context: AbstractDataContext):
        """
        Prepare a checkpoint.

        Args:
            config: The configuration.
            data_context: The data context.
        """
        logging.info("Preparing checkpoint...")
        cp_config = self.cp_template_handler.process_template(config)
        data_context.add_checkpoint(**cp_config)

    def run_checkpoint(self, config: dict[str, Any], data_context: AbstractDataContext) -> dict[str, Any]:
        """
        Run a checkpoint.

        Args:
            config: The configuration.
            data_context: The data context.

        Returns:
            A dictionary containing the result of running the checkpoint.
        """
        logging.info("Running checkpoint...")
        cp_name = (config["Source"]["Name"]).lower() + '_cp'
        batch_type, batch_input = self.get_batch_request_parameters(config)
        result = dict(
            data_context.run_checkpoint(
                checkpoint_name=cp_name,
                batch_request={
                    "runtime_parameters": {batch_type: batch_input},
                    "batch_identifiers": {"default_identifier_name": "default_identifier"}
                }
            )
        )
        if self.generate_docs:
            self.build_data_docs(data_context)
        return result

    @staticmethod
    def build_data_docs(data_context: AbstractDataContext):
        """
        Build data docs.

        Args:
            data_context: The data context.
        """
        logging.info("Building data docs...")
        data_context.build_data_docs()


    @staticmethod
    def generate_summary_table(validation_results: dict[str, Any], success_threshold: Optional[float] = None) -> pd.DataFrame:
        """
        Generate a summary table from validation results.

        Args:
            validation_results: The validation results.

        Returns:
            A DataFrame containing the summary table.
        """
        logging.info("Generating summary table...")
        results = validation_results['_run_results'][next(iter(validation_results['_run_results']))]['validation_result']['results']

        # Define a list to store each row of the summary table
        rows = []

        # Loop through each result
        for result in results:
            # Define a dictionary to store the row data
            row = {}

            # Add general data
            row['expectation_type'] = result['expectation_config']['expectation_type']
            row['success'] = result['success']

            # Add data from the result section
            row_data = result['result']
            for key, value in row_data.items():
                # If the value is a list, join its elements into a string
                if isinstance(value, list):
                    value = ', '.join(str(v) for v in value)

                # Add the value to the row
                row[key] = value

            # Add the row to the list
            rows.append(row)

        # Create a DataFrame from the rows
        df = pd.DataFrame(rows)

        # Calculate some statistics
        success_rate = df['success'].mean() * 100
        num_evaluated_expectations = len(df)

        print(f"Success rate: {success_rate}%")
        print(f"Number of evaluated expectations: {num_evaluated_expectations}")
        if success_threshold is not None and success_rate < success_threshold:
            error_message = f"Validation failed: success rate {success_rate}% is below the threshold {success_threshold}%"
            logging.error(error_message)
            raise Exception(error_message)

        return df
    
    @staticmethod
    def get_batch_request_parameters(config: dict[str, Any]) -> tuple[Optional[str], Optional[str]]:
        """
        Get the batch request parameters based on the configuration dictionary.

        Args:
            config (dict): The configuration dictionary.

        Returns:
            A tuple containing the batch request parameter key and value.
        """
        logging.info("Getting batch request parameters...")
        properties = config.get("Source", {}).get("Properties", {})
        
        if "InMemory" in properties:
            dataframe_name = properties["InMemory"].get("DataFrameName")
            if dataframe_name not in globals():
                raise ValueError(f"No dataframe exists in global scope with name {dataframe_name}")
            return "batch_data", globals()[dataframe_name]
        
        if "File" in properties:
            return "path", properties["File"].get("FilePath")
        logging.warning("No batch request parameters found in the configuration.")
        return None, None
