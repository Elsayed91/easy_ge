<a name="readme-top"></a>



<br />
<div align="center">
  <a href="">
    <img src="images/gewrap.png" alt="Logo" width="150" height="150">
  </a>

  <h3 align="center">Easy G.E — A Great Expectations Wrapper</h3> 
    <p align="center">Making Data Validation The Easiest Part of the Pipeline</p>
  <!-- <img src="https://img.shields.io/badge/build-passing-brightgreen"> <img src="https://img.shields.io/badge/license-MIT-blue"> -->

</div>



Ever wanted to implement some data quality checks as a part of your pipeline, but found yet another learning curve that you need to go through if you wanna use **Great Expectations**? Well, that's where **Easy G.E** (pronounced as _ee-zee-jee-ee_) comes in! For most common use cases, this package has your back and you will be ready to run your tests within minutes without having to ever go through Great Expectations every changing documentation.
**Great Expectations** is a crucial tool for validating the quality of your data. However, it may be a bit challenging for those who are not regular users. 


### Quick Start

#### Installation

You can install Easy G.E via pip:

```bash
pip install easy_ge
```

#### Usage

##### Configuration

Easy G.E uses a YAML configuration file. Here are a few examples of how to set it up:

| Scenario | Configuration |
|----------|---------------|
| Reading from a local CSV file and storing results on the local filesystem | [Example](examples/file_on_local_filesystem_config.yaml) |
| Reading from an in-memory DataFrame and storing results on Google Cloud Storage | [Example](examples/in_memory_save_to_gcs_config.yaml) |
| Reading from a local Parquet file and storing results on Amazon S3 | [Example](examples/local_file_to_s3_config.yaml) |


Once you have your configuration set up, you can run Easy G.E with the following code:

```python
from easy_ge.main import main

config_path = "path/to/your/config.yaml"
schema_path = "path/to/schema.json"
df = main(config_path, schema_path)
```

The `main` function will return a summary table of the validation results as a pandas DataFrame.

For more detailed usage instructions and configuration options, please see the examples provided in the `examples` directory.
### Docker

### Instructions

We provide two Docker images for running the validation: one with Python 3.10 and one with Apache Spark 3.3.1. You can pull the images from Docker Hub and run them with the following commands:

```bash
# Pull and run with Python 3.10
docker pull elsayed91/easy_ge:python3.10
docker run -v /path/to/config.yaml:/data/config.yaml image_name
```

### Key Features

-   **Easy Configuration**: Set up your data expectations using a YAML configuration file.
-   **Multiple Data Formats**: Supports both Pandas and Spark dataframes.
-   **Flexible Data Input**: Accepts data from a local file or an in-memory dataframe.
-   **Automatic Validation**: Automatically runs data validation and generates reports.
-   **Detailed Summary**: Provides a summary table of the validation results.
-   **Flexible Storage Options**: Store your data expectations on your local filesystem or in the cloud (supports both GCS and S3).

For more detailed usage instructions and configuration options, please see the examples provided in the `examples` directory.

## Roadmap

While Easy G.E already has a host of features to simplify your data expectations workflow, we're not stopping here. We believe there's always room for growth and improvement. Here are some future enhancements we're considering:

### Azure Support

We're planning to incorporate Azure into our list of supported cloud storage platforms. This means you'll soon be able to store your data expectations on Azure, making Easy G.E even more versatile and handy for users across different platforms.


### Acknowledgements

Easy G.E is not possible without the fantastic work done by the Great Expectations team. A huge thank you to them for making data quality expectations a reality!

## Known Issues

### Issue with jsonschema in Python 3.10

There is a known issue with the `jsonschema` package when running this project in Python 3.10. This may cause an error when trying to validate the configuration file against the JSON schema.

**Workaround:**

We recommend using a virtual environment

## Contribution & Support

If you encounter any problems or have any questions, please open an issue on our GitHub repository.
Feel free to contribute with a pull request or just request a feature.
