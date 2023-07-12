# tests/test_template_handler.py

import pytest
from easy_ge.helpers import TemplateHandler
from jinja2 import Template, TemplateNotFound


def test_load_and_render_template():
    # Test a valid template
    template_path = "easy_ge/templates/great_expectations.tpl"
    template_handler = TemplateHandler(template_path)
    context = {
        "Source": {"Name": "Test", "Processor": "Test", "Properties": {"File": {"FilePath": "test.yaml"}}},
        "Backend": {"ExpectationSuiteName": "Test", "GCS": {"Project": "Test", "Bucket": "Test"}},
        "Report": {"NamingRegex": "%Y%m%d%H%M-Test"},
        "Outputs": {"GenerateDocs": True}
    }
    try:
        rendered_template = template_handler._load_and_render_template(context)
        assert isinstance(rendered_template, str)
    except Exception as e:
        pytest.fail(f"Exception {type(e).__name__} was raised.")

    # Test an invalid template
    template_path = "templates/invalid_template.tpl"
    template_handler = TemplateHandler(template_path)
    with pytest.raises(FileNotFoundError):
        template_handler._load_and_render_template(context)

def test_convert_yaml_to_dict():
    config_str = """
    Source:
      Name: Test
      Processor: Test
      Properties: 
        File:
          FilePath: "test.yaml"
    """
    template_handler = TemplateHandler("")
    config_dict = template_handler._convert_yaml_to_dict(config_str)
    assert isinstance(config_dict, dict)
    assert config_dict["Source"]["Name"] == "Test"

def test_process_template():
    template_path = "easy_ge/templates/great_expectations.tpl"
    context = {
        "Source": {"Name": "Test", "Processor": "Test", "Properties": {"File": {"FilePath": "test.yaml"}}},
        "Backend": {"ExpectationSuiteName": "Test", "GCS": {"Project": "Test", "Bucket": "Test"}},
        "Report": {"NamingRegex": "%Y%m%d%H%M-Test"},
        "Outputs": {"GenerateDocs": True}
    }
    template_handler = TemplateHandler(template_path)
    processed_template = template_handler.process_template(context)
    assert isinstance(processed_template, dict)
    assert processed_template["datasources"]["Test"]["execution_engine"]["class_name"] == "TestExecutionEngine"
