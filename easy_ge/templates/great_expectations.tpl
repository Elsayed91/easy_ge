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
      prefix: {{ Backend.GCS.Prefix | default('', true) }}/expectations
      {% elif Backend.S3 %}
      class_name: TupleS3StoreBackend
      bucket: {{ Backend.S3.Bucket }}
      prefix: {{ Backend.S3.Prefix | default('', true) }}/expectations
      {% if Backend.S3.BotoEndpoint or Backend.S3.Region %}
      boto3_options:
        {% if Backend.S3.BotoEndpoint %}
        endpoint_url: {{ Backend.S3.BotoEndpoint }}
        {% endif %}
        {% if Backend.S3.Region %}
        region_name: {{ Backend.S3.Region }}
        {% endif %}
      {% endif %}
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
      prefix: {{ Backend.GCS.Prefix | default('', true) }}/validations
      {% elif Backend.S3 %}
      class_name: TupleS3StoreBackend
      bucket: {{ Backend.S3.Bucket }}
      prefix: {{ Backend.S3.Prefix | default('', true) }}/validations
      {% if Backend.S3.BotoEndpoint or Backend.S3.Region %}
      boto3_options:
        {% if Backend.S3.BotoEndpoint %}
        endpoint_url: {{ Backend.S3.BotoEndpoint }}
        {% endif %}
        {% if Backend.S3.Region %}
        region_name: {{ Backend.S3.Region }}
        {% endif %}
      {% endif %}
      {% endif %}
  evaluation_parameter_store:
    class_name: EvaluationParameterStore
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
      prefix: {{ Backend.GCS.Prefix | default('', true) }}/checkpoints
      {% elif Backend.S3 %}
      class_name: TupleS3StoreBackend
      bucket: {{ Backend.S3.Bucket }}
      prefix: {{ Backend.S3.Prefix | default('', true) }}/checkpoints
      {% if Backend.S3.BotoEndpoint or Backend.S3.Region %}
      boto3_options:
        {% if Backend.S3.BotoEndpoint %}
        endpoint_url: {{ Backend.S3.BotoEndpoint }}
        {% endif %}
        {% if Backend.S3.Region %}
        region_name: {{ Backend.S3.Region }}
        {% endif %}
      {% endif %}
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
      prefix: {{ Backend.GCS.Prefix | default('', true) }}/docs
      {% elif Backend.S3 %}
      class_name: TupleS3StoreBackend
      bucket: {{ Backend.S3.Bucket }}
      prefix: {{ Backend.S3.Prefix | default('', true) }}/docs
      {% if Backend.S3.BotoEndpoint or Backend.S3.Region %}
      boto3_options:
        {% if Backend.S3.BotoEndpoint %}
        endpoint_url: {{ Backend.S3.BotoEndpoint }}
        {% endif %}
        {% if Backend.S3.Region %}
        region_name: {{ Backend.S3.Region }}
        {% endif %}
      {% endif %}
      {% endif %}
    site_index_builder:
      class_name: DefaultSiteIndexBuilder
