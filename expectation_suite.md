# A Novice's Guide to Creating an Expectation Suite in Great Expectations

## What is an Expectation Suite?

An Expectation Suite in Great Expectations is a collection of expectations about your data. Each expectation is a rule that your data should adhere to. An Expectation Suite allows you to validate your data and make sure it meets your requirements.

## Step-by-Step Tutorial

### 1\. Initialization: Create the `.json` File

Initiate by creating a `.json` file that will store your expectations.

```bash
touch myexpectations.json
```

Then, populate the file with the basic structure as follows:

```json
{
    "data_asset_type": null, 
    "expectation_suite_name": "your_expectation_name",
    "expectations": []
}
```

Within "expectations": [], you'll insert the following code for each test you plan to execute, so if u have 2 tests, the content of your expectations list should look like this:

```json
        {
            "expectation_type": "PLACEHOLDER1 ",
            "kwargs": {
                "column": "PLACEHOLDER1"
            },
            "meta": {}
        },
        {
            "expectation_type": "PLACEHOLDER2",
            "kwargs": {
                "column": "PLACEHOLDER2"
            },
            "meta": {}
        },
```



### 2. Create an Expectation

Each expectation in your suite will be represented as a JSON object, comprising an `expectation_type` and a `kwargs` object. The `kwargs` object describes the specific parameters of the expectation.

```json
{
    "data_asset_type": null,
    "expectation_type": "<Expectation Test Name Here>",
    "kwargs": {
        "column": "<Column Name Here>",
        ...
    }
}
```

### 3. Customize Your Expectation with kwargs

The `kwargs` object in each expectation is where you define the specific parameters for the expectation. Different expectations have different `kwargs`, but some common ones include:

- `column`: The column in your dataset that the expectation is applied to.
- `min_value` and `max_value`: The minimum and maximum values for the column, used in expectations like `expect_column_values_to_be_between`.
- `mostly`: A percentage that determines how many values in the column must pass the expectation for it to be considered successful. For instance, a `mostly` value of 0.95 means the expectation must pass for 95% of the values.
- `strict_min` and `strict_max`: Determine whether the `min_value` and `max_value` are inclusive or exclusive.
- `value_set`: A list of values that a column's values should match, used in expectations like `expect_column_values_to_be_in_set`.


```json
{
    "expectation_type": "expect_column_values_to_be_between",
    "kwargs": {
        "column": "<Your Column Name Here>",
        "min_value": <Your Minimum Value Here>,
        "max_value": <Your Maximum Value Here>,
        "mostly": <Your 'Mostly' Value Here>,
        "strict_min": <True/False>,
        "strict_max": <True/False>
    }
}
```

### 4. Include Metadata (Optional)

You can also include metadata about your Expectation Suite or individual expectations using the `meta` object. This can be useful for adding notes or comments.

```json
"meta": {
    "notes": {
        "format": "markdown",
        "content": ["<Your Notes or Comments Here>"]
    }
}
```

### 5. Repeat for Each Expectation

Repeat the process of creating and customizing expectations for each expectation you want to include in your suite.

### 6. Complete Suite

In the end, your Expectation Suite might look something like this:

```json
{
    "expectation_suite_name": "<Your Expectation Suite Name Here>",
    "expectations": [
        {
            "expectation_type": "expect_column_values_to_be_between",
            "kwargs": {
                "column": "<Your Column Name Here>",
                "min_value": <Your Minimum Value Here>,
                "max_value": <Your Maximum Value Here>,
                "mostly": <Your 'Mostly' Value Here>,
                "strict_min": <True/False>,
                "strict_max": <True/False>
            },
            "meta": {
                "notes": {
                    "format": "markdown",
                    "content": ["<Your Notes or Comments Here>"]
                }
            }
        },
        ...
    ]
}
```

You can add as many expectations to your suite as you need, each with its own specific `kwargs`.

### 7. Save and Use Your Suite

Lastly, save your JSON document in an `/expectations` directory and use the filename (without `.json`) in the `ExpectationSuiteName` field to implement your suite with `Easy GE`.

```yaml
Source:
  Name: your_report_name
  Processor: Pandas
  Properties:
    InMemory:
      DataFrameName: your_declared_dataframe
      
Backend:
  ExpectationSuiteName: myexpectations
  Filesystem:
    WorkDir: /path/to/your/local/workdir
    
Report:
  NamingRegex: "%Y%m%d%H%M-report"
  
Outputs:
  GenerateDocs: True
```

And that's it! You've created an Expectation Suite in Great Expectations. Remember, the actual expectations and parameters you use will depend heavily on your specific data and use case. Visit the [Expectations Gallery](https://greatexpectations.io/expectations/?viewType=Completeness&filterType=Backend+support&showFilters=true&subFilterValues=) for a comprehensive list of available Expectations and their options to employ in your tests.