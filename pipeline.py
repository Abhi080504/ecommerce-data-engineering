
import logging
import subprocess
import sys
from pathlib import Path

# Configure timestamped logging for the pipeline.
# This controls the log level and the format of each log message.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Create a logger for this module.
# We use it to record pipeline progress and errors.
logger = logging.getLogger(__name__)

# Find the project root based on this file's location.
# This avoids hard-coding a Windows directory path.
BASE_DIR = Path(__file__).resolve().parent

# Use the same Python interpreter that runs this pipeline.
# This helps ensure the child scripts use the active virtual environment.
PYTHON = sys.executable

# Define the ETL stages in the order they must execute:
# Extract -> Clean -> Improve data quality -> Load into MySQL.
STAGES = [
    "src/ingestion/api_ingestion.py",
    "src/transformation/clean_products.py",
    "src/transformation/improve_product_quality.py",
    "src/loaders/load_products.py",
]


def run_stage(stage):
    """Execute one ETL stage and report its status."""

    # Build the full path to the script being executed.
    script_path = BASE_DIR / stage

    # Log which stage is starting.
    logger.info("Starting stage: %s", stage)

    try:
        # Launch the script as a separate Python process.
        subprocess.run(
            [PYTHON, str(script_path)],
            cwd=BASE_DIR,  # Run from the project root.
            check=True,    # Raise an error if the script fails.
        )

    except subprocess.CalledProcessError:
        # Record the error details, including the traceback.
        logger.exception("Stage failed: %s", stage)

        # Pass the error to the main pipeline handler.
        raise

    # This message appears only when the stage succeeds.
    logger.info("Completed stage: %s", stage)


def run_pipeline():
    """Execute all ETL stages in sequence."""

    # Record the start of the overall pipeline.
    logger.info("ETL pipeline started")

    # Run each stage in the order defined in STAGES.
    # If a stage fails, the exception stops subsequent stages.
    for stage in STAGES:
        run_stage(stage)

    # This message appears only after every stage succeeds.
    logger.info("ETL pipeline completed successfully")


if __name__ == "__main__":
    # This block runs only when pipeline.py is executed directly.
    try:
        run_pipeline()

    except subprocess.CalledProcessError:
        # Log the overall failure and return a non-zero exit code.
        logger.error("ETL pipeline failed")
        sys.exit(1)
