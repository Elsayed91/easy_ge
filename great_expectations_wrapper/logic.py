from great_expectations.data_context import BaseDataContext
from great_expectations.data_context.types.base import DataContextConfig

from helpers import ConfigLoader, TemplateHandler


def replace_batch_data_with_global_variable(config: dict) -> dict:
    """
    Replace the value of `batch_data` in the config dictionary with its corresponding global variable.

    Args:
        config (dict): The config dictionary.

    Returns:
        The updated config dictionary, or the original dictionary if `batch_data` is not found.

    Raises:
        KeyError: If no global variable exists with the name specified in `batch_data`.
    """
    # Iterate over each validation in the config
    for validation in config.get("validations", []):
        runtime_parameters = validation.get("batch_request", {}).get("runtime_parameters", {})
        
        # If `batch_data` exists, try to replace its value with the corresponding global variable
        if "batch_data" in runtime_parameters:
            old_value = runtime_parameters["batch_data"]
            try:
                runtime_parameters["batch_data"] = globals()[old_value]
                return config  # Return early after making the replacement
            except KeyError:
                # Raise a more descriptive error message
                raise KeyError(f"No DataFrame exists in global scope with name {old_value}")

    # If `batch_data` is not found, return the original config
    return config



import numpy as np
import pandas as pd

df = pd.DataFrame({
        "PULocationID": np.random.randint(1, 10, 100),
        "DOLocationID": np.random.randint(1, 10, 100),
    })

if __name__ == "__main__":
    config_path = "sample_config.yaml"
    schema_path = "schema.json"
    path_to_ge_template = "templates/great_expectations.tpl"
    path_to_cp_template = "templates/checkpoint.tpl"
    user_input = ConfigLoader(config_path, schema_path).load_config()
    ge_config = TemplateHandler(path_to_ge_template).process_template(user_input)
    cp_config = TemplateHandler(path_to_cp_template).process_template(user_input)

    print((user_input["Source"]["Name"]).lower())
    # If the source is in memory, replace `batch_data` with the global variable
    # if user_input.get('Source', {}).get('Properties', {}).get('InMemory', None) is not None:
    #     cp_config = replace_batch_data_with_global_variable(cp_config)
    # # # Create the DataContext
    # data_context = BaseDataContext(DataContextConfig(**ge_config))

    # # # Add the checkpoint to the DataContext
    # data_context.add_checkpoint(**cp_config)
    # cp_result = dict(data_context.run_checkpoint(checkpoint_name=user_input["Source"]["Name"]))
    # data_context.build_data_docs()
