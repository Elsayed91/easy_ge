config_version: 3

datasources:
  {{ Source.Name }}:
    module_name: great_expectations.datasource
    class_name: Datasource
    execution_engine:
      module_name: great_expectations.execution_engine
      class_name: {{ Source.Processor }}ExecutionEngine
    data_connectors:
      default_runtime_data_connector_name:
        class_name: RuntimeDataConnector
        batch_identifiers:
          - default_identifier_name

stores:
  expectations_store:
    class_name: ExpectationsStore
    store_backend:
      {% if Backend.Filesystem %}
      class_name: TupleFilesystemStoreBackend
      base_directory: {{ Backend.Filesystem.WorkDir }}/expectations/
      {% elif Backend.GCS %}
      class_name: TupleGCSStoreBackend
      project: {{ Backend.GCS.Project }}
      bucket: {{ Backend.GCS.Bucket }}
      prefix: {{ Backend.GCS.Prefix | default('expectations', true) }}
      {% elif Backend.S3 %}
      class_name: TupleS3StoreBackend
      bucket: {{ Backend.S3.Bucket }}
      prefix: {{ Backend.S3.Prefix | default('expectations', true) }}
      {% endif %}
  validations_store:
    class_name: ValidationsStore
    store_backend:
      {% if Backend.Filesystem %}
      class_name: TupleFilesystemStoreBackend
      base_directory: {{ Backend.Filesystem.WorkDir }}/validations/
      {% elif Backend.GCS %}
      class_name: TupleGCSStoreBackend
      project: {{ Backend.GCS.Project }}
      bucket: {{ Backend.GCS.Bucket }}
      prefix: {{ Backend.GCS.Prefix | default('validations', true) }}
      {% elif Backend.S3 %}
      class_name: TupleS3StoreBackend
      bucket: {{ Backend.S3.Bucket }}
      prefix: {{ Backend.S3.Prefix | default('validations', true) }}
      {% endif %}
  evaluation_parameter_store:
    class_name: EvaluationParameterStore
    store_backend:
      {% if Backend.Filesystem %}
      class_name: TupleFilesystemStoreBackend
      base_directory: {{ Backend.Filesystem.WorkDir }}/evaluation_parameters/
      {% elif Backend.GCS %}
      class_name: TupleGCSStoreBackend
      project: {{ Backend.GCS.Project }}
      bucket: {{ Backend.GCS.Bucket }}
      prefix: {{ Backend.GCS.Prefix | default('evaluation_parameters', true) }}
      {% elif Backend.S3 %}
      class_name: TupleS3StoreBackend
      bucket: {{ Backend.S3.Bucket }}
      prefix: {{ Backend.S3.Prefix | default('evaluation_parameters', true) }}
      {% endif %}
  checkpoint_store:
    class_name: CheckpointStore
    store_backend:
      {% if Backend.Filesystem %}
      class_name: TupleFilesystemStoreBackend
      base_directory: {{ Backend.Filesystem.WorkDir }}/checkpoints/
      {% elif Backend.GCS %}
      class_name: TupleGCSStoreBackend
      project: {{ Backend.GCS.Project }}
      bucket: {{ Backend.GCS.Bucket }}
      prefix: {{ Backend.GCS.Prefix | default('checkpoints', true) }}
      {% elif Backend.S3 %}
      class_name: TupleS3StoreBackend
      bucket: {{ Backend.S3.Bucket }}
      prefix: {{ Backend.S3.Prefix | default('checkpoints', true) }}
      {% endif %}

expectations_store_name: expectations_store
validations_store_name: validations_store
evaluation_parameter_store_name: evaluation_parameter_store
checkpoint_store_name: checkpoint_store

data_docs_sites:
  {{ Source.Name }}Docs:
    class_name: SiteBuilder
    store_backend:
      {% if Backend.Filesystem %}
      class_name: TupleFilesystemStoreBackend
      base_directory: {{ Backend.Filesystem.WorkDir }}/docs
      {% elif Backend.GCS %}
      class_name: TupleGCSStoreBackend
      project: {{ Backend.GCS.Project }}
      bucket: {{ Backend.GCS.Bucket }}
      prefix: {{ Backend.GCS.Prefix | default('docs', true) }}
      {% elif Backend.S3 %}
      class_name: TupleS3StoreBackend
      bucket: {{ Backend.S3.Bucket }}
      prefix: {{ Backend.S3.Prefix | default('docs', true) }}
      {% endif %}
    site_index_builder:
      class_name: DefaultSiteIndexBuilder
