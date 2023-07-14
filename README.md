<a name="readme-top"></a>


<div align="center"> 
  <a href=""> <img src="images/gewrap.png" alt="Logo" width="150" height="150"> </a>
  <h3 align="center">Easy G.E — Your Friendly Great Expectations Wrapper</h3> 
  <p align="center">Simplifying Data Validation in Your Pipeline</p> 
  </div>

Are you looking to integrate data quality checks into your pipeline but daunted by the
learning curve associated with **Great Expectations**? Let **Easy G.E** (_pronounced
ee-zee-jee-ee_) come to your rescue. It is designed for common use cases, enabling you to
set up tests in minutes and saving you from navigating through Great Expectations'
continuously evolving documentation.

## Quick Start

### Installation

Easy G.E has been tested exclusively on Python versions >= 3.10.

Installation is via pip:

```bash
pip install easy-ge # for gcs use pip install easy-ge[google]
```

### Usage

1.  **Create Your Expectation Suite:** This comprises the tests that will be run on your table and/or columns. Here is an example:

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

Check [here](examples/example_expectation_suite.json) for a more extensive example, and visit the [Expectations Gallery](https://greatexpectations.io/expectations/?viewType=Completeness&filterType=Backend+support&showFilters=true&subFilterValues=) for a full list of available Expectations.

    
2.  **Create Your Configuration File:** Something Like this:
    

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
You can find different examples of configurations in [this directory](examples/).

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


## Roadmap

On the todo list are:

1. Azure
2. Profiler
3. Custom Expectations support
4. Flexible Backend Setup; the current implementation simplifies the matter by using the same backend for all stores, this will remain the main appraoch, but providing the option to customize them if needed is on the to-do list.



## Known Issues

### Issue with jsonschema

If you face any issues when running the package because `jsonschema`, installing the package in a virtualenv will resolve it.
`jsonschema` could run into dependency issues if the package is not installed in a virtualenv. 


### Acknowledgements

Easy G.E wouldn't be possible without the substantial efforts by the Great Expectations team.

## Contribution & Support

Should you face any issues or have queries, please open an issue.
Contributions are welcome, be it through pull requests or feature requests.

