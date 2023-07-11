import json
import os
from typing import Any

import yaml
from jinja2 import Template
from jsonschema import ValidationError as JsonSchemaValidationError
from jsonschema import validate


class ValidationError(Exception):
    """Validation Unsuccessful"""


class ConfigLoader:
    """
    A class for loading, parsing, and validating YAML configuration files,
    substituting the values of environmental variables.
    The variables must match the format ${VARIABLE} to be substituted.
    Usage Example: config = ConfigLoader("/path/to/yaml").load_config()
    """

    def __init__(self, config_path: str, schema_path: str):
        self.config_path = config_path
        self.schema_path = schema_path

    def substitute_env_variables(self, data):
        """
        Recursively substitutes the values of environmental variables
        in the given data structure.

        Args:
            data: The data structure to process. Can be a dictionary, list, or string.

        Returns:
            The data structure with the environmental variables substituted.
        """
        if isinstance(data, dict):
            for key, value in data.items():
                data[key] = self.substitute_env_variables(value)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                data[i] = self.substitute_env_variables(item)
        elif isinstance(data, str) and data.startswith("${") and data.endswith("}"):
            # This is an environmental variable. Substitute its value.
            var_name = data[2:-1]
            data = os.getenv(var_name)
        return data

    def load_config(self):
        """
        Loads and parses the YAML configuration file,
        substituting the values of environmental variables.

        Returns:
            The parsed configuration data with the environmental variables substituted.
        """
        # Load the YAML file
        with open(self.config_path, "r") as f:
            data = yaml.safe_load(f)

        # Substitute the values of the environmental variables
        self.substitute_env_variables(data)

        # Load the JSON schema
        with open(self.schema_path, "r") as f:
            schema = json.load(f)

        # Validate the configuration against the schema
        try:
            validate(data, schema)
        except JsonSchemaValidationError as err:
            raise ValidationError(f"Configuration validation error: {err.message}")

        print("Loaded and Validated Successfully.")
        return data

class TemplateHandler:
    """
    A class for handling Jinja2 templates.
    """

    def __init__(self, template_path: str):
        self.template_path = template_path

    def load_template(self) -> Template:
        """
        Load a Jinja2 template from a file.

        Returns:
            A Jinja2 Template object.
        """
        with open(self.template_path, "r") as template_file:
            template = Template(template_file.read())
        return template

    def render_template(self, template: Template, context: dict) -> str:
        """
        Render a Jinja2 template with a given context.

        Args:
            template: The Jinja2 Template object.
            context: The context to render the template with.

        Returns:
            The rendered template as a string.
        """
        return template.render(**context)

    def convert_to_dict(self, config_str: str) -> dict:
        """
        Convert a YAML configuration string to a dictionary.

        Args:
            config_str: The YAML configuration string.

        Returns:
            The configuration as a dictionary.
        """
        return yaml.safe_load(config_str)

    def process_template(self, context: dict) -> dict:
        """
        Load, render and convert a Jinja2 template to a dictionary.

        Args:
            context: The context to render the template with.

        Returns:
            The processed template as a dictionary.
        """
        template = self.load_template()
        rendered_template = self.render_template(template, context)
        return self.convert_to_dict(rendered_template)
