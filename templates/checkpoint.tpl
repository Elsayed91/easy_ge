# checkpoint.yaml validations
name: {{ Source.Name | lower }}_cp
config_version: 1
class_name: Checkpoint
run_name_template: "{{ Report.NamingRegex }}"
validations:
  - batch_request:
      datasource_name: {{ Source.Name }}
      data_connector_name: default_runtime_data_connector_name
      data_asset_name: {{ Source.Name }}Data
      batch_identifiers:
        default_identifier_name: default_identifier
      {% if Source.Properties.File %}
      runtime_parameters:
        path: {{ Source.Properties.File.FilePath }}
      {% endif %}
    expectation_suite_name: {{ Source.Name }}Tests
    action_list:
      - name: store_validation_result
        action:
          class_name: StoreValidationResultAction
      - name: store_evaluation_params
        action:
          class_name: StoreEvaluationParametersAction
      {% if Outputs.GenerateDocs %}
      - name: update_data_docs
        action:
          class_name: UpdateDataDocsAction
      {% endif %}
    {% if Outputs.ResultsDict.Save %}
    runtime_configuration:
      result_format:
        result_format: {{ Outputs.ResultsDict.Format }}
    {% endif %}
