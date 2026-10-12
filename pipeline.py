"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --output clean.csv
    python pipeline.py --input data.csv --output results.json --verbose
"""

import argparse
import logging
import sys

import pandas as pd

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)

logger = logging.getLogger(__name__)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Data Processing Pipeline"
    )

    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Path to input file"
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to YAML configuration file"
    )

    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Path to output file"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    return parser.parse_args()


def main() -> None:
    """Main pipeline function."""
    args = parse_arguments()

    setup_logging(args.verbose)

    logger.debug(
        "Arguments parsed: input=%s, output=%s, config=%s",
        args.input, args.output, args.config
    )

    if not validate_input(args.input):
        sys.exit(1)

    if not validate_input(args.config):
        sys.exit(1)

    try:
        data = load_data(args.input)
        config = load_data(args.config)

        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be a CSV DataFrame")

        if not isinstance(config, dict):
            raise ValueError("Configuration must be a dictionary")

    except (ValueError, OSError) as error:
        logger.error("Failed to load data: %s", error)
        sys.exit(1)

    required_columns = config["validation"]["required_columns"]
    numeric_columns = config["validation"]["numeric_columns"]

    rows_before_validation = len(data)

    try:
        data = validate_dataframe(data, required_columns, numeric_columns)

    except ValueError as error:
        logger.error("Data validation failed: %s", error)
        sys.exit(1)

    logger.info(
        "Validation complete: %d -> %d rows",
        rows_before_validation,
        len(data)
    )

    original_data = data.copy()

    try:
        cleaned_data = process_data(data, config)

    except ValueError as error:
        logger.error("Data processing failed: %s", error)
        sys.exit(1)

    logger.info(
        "Processing complete: %d -> %d rows",
        len(original_data),
        len(cleaned_data)
    )

    save_data(cleaned_data, args.output)
    logger.info("Saved cleaned data to %s", args.output)

    report = create_cleaning_report(original_data, cleaned_data)
    print("Cleaning report:")
    print(report)


if __name__ == "__main__":
    main()