
"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --output clean.csv
    python pipeline.py --input data.csv --output results.json --format json --verbose
"""

import argparse
import logging
import sys
from pathlib import Path
from data_loaders import load_data
import pandas as pd
import yaml
from data_processor import process_data, create_cleaning_report


logger = logging.getLogger(__name__)



def setup_logging(verbose: bool = False) -> None:
    """Configure logging for the pipeline."""
    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%H:%M:%S"
    )




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




def validate_input(filepath: str) -> bool:
    """Check whether the input path exists and is a file."""
    if Path(filepath).is_file():
        logger.info(f"Input file validated: {filepath}")
        return True
    else:
        logger.error(f"Input file not found: {filepath}")
        return False





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

    
    try:
        data = load_data(args.input)
        logger.info("Data loaded successfully")
        logger.debug("Loaded data: %s", data)

        if isinstance(data, pd.DataFrame):
            with open(args.config, "r", encoding="utf-8") as file:
                config = yaml.safe_load(file)

            cleaned_data = process_data(data, config)
            report = create_cleaning_report(data, cleaned_data)

            cleaned_data.to_csv(args.output, index=False)
            logger.info("Cleaned data saved to %s", args.output)

            logger.info("Data cleaning completed")
            logger.info("Cleaning report: %s", report)
        else:
            logger.info("Input is not a CSV DataFrame; skipping cleaning")

    except (ValueError, OSError, yaml.YAMLError, KeyError) as error:
        logger.error("Pipeline failed: %s", error)
        sys.exit(1)




if __name__ == "__main__":
    main()
