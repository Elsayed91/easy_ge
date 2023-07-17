<a name="readme-top"></a>


<div align="center"> 
  <a href=""> <img src="docs/images/gewrap.png" alt="Logo" width="150" height="150"> </a>
  <h3 align="center">Easy G.E — Your Friendly Great Expectations Wrapper</h3> 
  <p align="center">Simplifying Data Validation in Your Pipeline</p> 
  </div>

Want to integrate data quality checks into your pipeline but daunted by the
learning curve associated with **Great Expectations**? **Easy G.E** (_pronounced
ee-zee-jee-ee_) comes to rescue. It is designed for common use cases (In Memory/File), enabling you to
set up tests in minutes and saving you from navigating through Great Expectations'
continuously evolving (or rather ever-changing) documentation.


## Quick Start

### Installation

Note: Easy G.E has been tested exclusively on Python versions >= 3.10.

Installation is via pip:

```bash
pip install easy-ge # for gcs use pip install easy-ge[google]
```

### Usage

1.  **Create Your Expectation Suite:** This comprises the tests that will be run on your table and/or columns. Below is an example of the content of an expectation suite json file:

```json
{
    "data_asset_type": null,
    "expectation_suite_name": "yellow_expectations",
    "expectations": [
        {
            "expectation_type": "expect_column_max_to_be_between",
            "kwargs": {
                "column": "DOLocationID",
                "max_value": 265,
                "min_value": 1,
                "mostly": 0.9
            },
            "meta": {}
        }
    ]
}

```

Check [here](examples/example_expectation_suite.json) for a more extensive example, [here](expectation_suite.md) for a tutorial, and visit the [Expectations Gallery](https://greatexpectations.io/expectations/?viewType=Completeness&filterType=Backend+support&showFilters=true&subFilterValues=) for a full list of available Expectations (and their options) to use for your own tests.

    
2.  **Create Your Configuration File:**
    

```yaml
# You can use the ${VAR} syntax anywhere in the file to replace them with the corresponding runtime Python environment variable values.

Source: # data/file origin
  Name: test  # Assigned name for the data source
  Processor: Pandas  # Can be "SparkDF" or "Pandas"
  Properties:
    File:
      FilePath: "tests/test_configs/sample_file.csv"

Backend: # where artifacts/docs will be stored
  ExpectationSuiteName: yellow #Expectation suite JSON file name (without .json)
  GCS:
    Project: ${PROJECT} 
    Bucket: ${BUCKET}

Report:
  NamingRegex: "%Y%m%d%H%M-yellow" # Report naming format

Outputs:
  GenerateDocs: True

```
The above is an example. You can find different examples of configurations in [this directory](examples/).



3. **Position the Expectation Suite:** Place the suite file where you want your docs to be stored. For instance, if you want your docs in a GCS bucket, put the expectation suite in an `expectations` folder within that bucket. this bucket has to be in the same location as your backend.

4.  **Import the `easy_validation` Function:**

```python
import os
from easy_ge import easy_validation

# Authenticate if using a cloud backend.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp_key.json"

# Populate a variable declared in the manifest that doesn't exist in the original environment.
os.environ["project"] = "Stellarismusv5"

if __name__ == '__main__':
    results = easy_validation("config.yaml")

```

5.  You're done! Check the chosen backend for your docs. Note that if you've enabled `SaveSummaryTableAsCSV`, you'll have a CSV file saved with test statistics. This table provides a quick overview of potential issues, offering detailed insights into problematic rows and undesired value counts, including indecies for these rows, allowing for closer inspection.



### Docker Usage

For validating your files on the fly, you can use the Docker image. However, this is applicable only for files as `InMemory` cannot be used. AWS & GCP will require credentials.

```bash
docker pull elsayed91/easy_ge:python3.10
docker run -v /path/to/config.yaml:/app/config.yaml \
    -v /path/to/key.json:/app/key.json \ #if using GCS
    -e GCS_CREDENTIALS_FILE="key.json" \ #if using GCS
    -e S3_ACCESS_KEY="your_aws_access_key" \ #if using S3
    -e S3_SECRET_KEY="your_aws_secret_key" \ #if using S3
    elsayed91/easy-ge --config /app/config.yaml
```

## Spark
Spark has been tested and is functional, howeverit's worth noting that PySpark is not included as a dependency. This is due to the requirement for Spark and PySpark versions to align perfectly. To utilize the `SparkDF` option, please ensure that your environment has both Spark and PySpark installed. 

## Roadmap

Enhancements on the radar:

-   Integration with Azure.
-   Profiler Support.
-   Support for custom Expectations.
-   Greater flexibility in Backend Setup: While the current design simplifies processes by using the same backend for all stores, providing options for customization in the future is on the agenda.
-   Defining Expectations as `Yaml` and/or in the same config file.
 

## Known Issues

### jsonschema

If you encounter problems running the package due to `jsonschema`, installing the package in a virtual environment should resolve the issue. Dependency conflicts with `jsonschema` may occur when the package is not installed in a virtual environment.


### Acknowledgements

- Easy G.E is an indirect product of the substantial efforts by the Great Expectations team.
- `ChatGPT` for helping with crafting some of the unit tests. 

## Contribution & Support

Should you face any issues or have inqueries, please open an issue. 

The package was designed with extensibility in mind.
Adjust `schema.json` if you want to add a new field in the YAML, then see how you want to use the new value.
If you are interested in contributing, you'd find it a breeze for the most part. 

The package was designed with extensibility in mind. To add a new field in the YAML, simply adjust the `schema.json` accordingly, and explore the possibilities of utilizing the new value in the `expectation_manager` class or the `run_validation` function. 

What am trying to say is, feel free to contribute. 