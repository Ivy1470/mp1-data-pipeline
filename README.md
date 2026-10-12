# MP1 Data Pipeline

This pipeline loads a CSV file, validates it, cleans it, and saves the result as a new CSV file using settings from a YAML configuration file. Data moves through the pipeline in order: it is loaded, validated (required columns and numeric values are checked), processed (duplicates, missing values, and outliers are removed), and then saved to the output folder. The file `pipeline.py` is the entry point that parses command-line arguments and coordinates every step. The `src/` folder holds the modules: `data_loaders.py` reads CSV, JSON, and YAML files, and `data_validator.py` checks required columns and removes rows with invalid numeric values. The module `data_processor.py` applies the configured cleaning steps and builds the cleaning report, `data_output.py` saves the cleaned DataFrame to CSV, and `utils.py` provides logging setup and input file checks. The file `config/config.yaml` stores the validation and processing settings, and `fixtures/` contains the test data.

## Example

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

Output:

```text
02:23:38 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, output=output/clean.csv, config=config/config.yaml
02:23:38 INFO     src.utils — Input file validated: fixtures/sample_data.csv
02:23:38 INFO     src.utils — Input file validated: config/config.yaml
02:23:38 INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
02:23:38 INFO     src.data_loaders — Loaded YAML file: config/config.yaml
02:23:38 WARNING  src.data_validator — Removing 2 rows with invalid numeric values in rating
02:23:38 DEBUG    src.data_validator — Validation completed: 100 -> 98 rows
02:23:38 INFO     __main__ — Validation complete: 100 -> 98 rows
02:23:38 DEBUG    src.data_processor — remove_duplicates: 98 -> 96 rows, removed=2
02:23:38 DEBUG    src.data_processor — handle_missing: removed 2 rows
02:23:38 DEBUG    src.data_processor — remove_outliers: method=iqr, threshold=1.5, removed=2 rows
02:23:38 INFO     __main__ — Processing complete: 98 -> 92 rows
02:23:38 DEBUG    src.data_output — Saved 92 rows to output/clean.csv
02:23:38 INFO     __main__ — Saved cleaned data to output/clean.csv
Cleaning report:
{'rows_before': 98, 'rows_after': 92, 'rows_removed': 6, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}
```