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
    expectation_suite_name: {{ Backend.ExpectationSuiteName }}
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
    {% if Outputs.SaveSummaryTableAsCSV %}
    runtime_configuration:
      result_format:
        result_format: COMPLETE
    {% endif %}
