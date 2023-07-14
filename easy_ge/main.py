"""
This module contains the main logic for the great_expectations_wrapper package.
"""

import importlib.resources
import logging
from datetime import datetime

try:
    from expectation_manager import ExpectationManager
    from helpers import ConfigLoader, TemplateHandler
except:
    from .expectation_manager import ExpectationManager
    from .helpers import ConfigLoader, TemplateHandler  

###############################
# ONLY FOR LOCAL Testing
###############################
GCP_KEY_PATH = "gcp_key_spark.json"
JAVA_HOME = "/usr/lib/jvm/java-11-openjdk-amd64"
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GCP_KEY_PATH
os.environ["JAVA_HOME"] = JAVA_HOME

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

def easy_validation(config: str):
    schema_path = importlib.resources.files("easy_ge.templates").joinpath("schema.json")
    ge_template_path = importlib.resources.files("easy_ge.templates").joinpath("great_expectations.tpl")
    cp_template_path = importlib.resources.files("easy_ge.templates").joinpath("checkpoint.tpl")

    user_config = ConfigLoader(config, str(schema_path)).load_config()

    ge_template_handler = TemplateHandler(str(ge_template_path))
    cp_template_handler = TemplateHandler(str(cp_template_path))
    
    expectation_manager = ExpectationManager(ge_template_handler, cp_template_handler, user_config["Outputs"]["GenerateDocs"])

    data_context = expectation_manager.prepare_data_context(user_config)
    expectation_manager.prepare_checkpoint(user_config, data_context)

    cp_result = expectation_manager.run_checkpoint(user_config, data_context)
    success_threshold = user_config["Outputs"].get("FailureThreshold", None)
    df = expectation_manager.generate_summary_table(cp_result, success_threshold)

    if user_config["Outputs"]["SaveSummaryTableAsCSV"]:
        logging.info("Saving summary table as CSV...")
        filename = f"{user_config['Backend']['ExpectationSuiteName']}-{datetime.today().strftime('%Y-%m-%d')}.csv"
        df.to_csv(filename)
    logging.info("Validation complete.")

    return df  # return the summary table

if __name__ == "__main__":
    config_path = "sample_config.yaml"
    df = easy_validation(config_path)
