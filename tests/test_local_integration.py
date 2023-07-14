import builtins
import json
import os

import pandas as pd
import pytest
import yaml
from easy_ge.main import easy_validation

df = pd.DataFrame({
    "PULocationID": [9, 7, 6, 5, 3, 8, 7, 1, 8, 8, 8, 3, 3, 6, 5],
    "DOLocationID": [6, 3, 2, 5, 6, 1, 2, 4, 5, 7, 5, 7, 8, 5, 8] })

@pytest.fixture
def in_memory_data():
    return pd.DataFrame({
        "PULocationID": [9, 7, 6, 5, 3, 8, 7, 1, 8, 8, 8, 3, 3, 6, 5],
        "DOLocationID": [6, 3, 2, 5, 6, 1, 2, 4, 5, 7, 5, 7, 8, 5, 8]
    })

@pytest.fixture
def local_file():
    df = pd.DataFrame({
        "PULocationID": [9, 7, 6, 5, 3, 8, 7, 1, 8, 8, 8, 3, 3, 6, 5],
        "DOLocationID": [6, 3, 2, 5, 6, 1, 2, 4, 5, 7, 5, 7, 8, 5, 8]
    })
    file_path = "tests/test_configs/sample_file.csv"
    df.to_csv(file_path, index=False)
    return file_path

@pytest.fixture
def expectations():
    with open("tests/test_configs/expectations/yellow.json") as f:
        return json.load(f)
    
def test_easy_validation_with_local_file(local_file, expectations):
    # Load configuration template
    with open("tests/test_configs/local_file_config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)

    # Convert relative paths in the configuration to absolute paths
    config['Backend']['Filesystem']['WorkDir'] = os.path.abspath(config['Backend']['Filesystem']['WorkDir'])
    config['Source']['Properties']['File']['FilePath'] = os.path.abspath(local_file)

    # Save the configuration to a new yaml file
    config_path = "tests/test_configs/local_file_config_w.yaml"
    with open(config_path, 'w') as outfile:
        yaml.dump(config, outfile, default_flow_style=False)

    summary_table = easy_validation(config_path)
    assert summary_table["expectation_type"].tolist() == [exp["expectation_type"] for exp in expectations["expectations"]]
    assert summary_table["success"].all()  # all expectations should pass






def test_easy_validation_with_in_memory_data(in_memory_data, expectations):
    # Define the DataFrame within the function
    df = pd.DataFrame({
        "PULocationID": [9, 7, 6, 5, 3, 8, 7, 1, 8, 8, 8, 3, 3, 6, 5],
        "DOLocationID": [6, 3, 2, 5, 6, 1, 2, 4, 5, 7, 5, 7, 8, 5, 8] })

    # Save the original globals function
    original_globals = builtins.globals

    # Define a new globals function that includes the DataFrame
    def new_globals():
        g = original_globals()  # Get the original globals
        g['df'] = df  # Add the DataFrame
        return g

    # Replace the original globals function with the new one
    builtins.globals = new_globals

    # Now, within this function, 'df' is in the global scope as far as easy_ge.expectation_manager is concerned
    # Load configuration template
    with open("tests/test_configs/in_memory_config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)

    # Convert relative paths in the configuration to absolute paths
    config['Backend']['Filesystem']['WorkDir'] = os.path.abspath(config['Backend']['Filesystem']['WorkDir'])

    # Save the configuration to a new yaml file
    config_path = "tests/test_configs/in_memory_config_w.yaml"
    with open(config_path, 'w') as outfile:
        yaml.dump(config, outfile, default_flow_style=False)

    summary_table = easy_validation(config_path)
    assert summary_table["expectation_type"].tolist() == [exp["expectation_type"] for exp in expectations["expectations"]]
    assert summary_table["success"].all()  # all expectations should pass

    # Restore the original globals function
    builtins.globals = original_globals
