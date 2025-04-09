import json
import pandas as pd
import argparse
import logging
import sys
from pathlib import Path
from typing import List, Dict, Any


def setup_logging():
    """Configure logging for the script."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("json_updater.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )


def load_csv_mapping(file_path: str, old_col: str, new_col: str) -> Dict[str, str]:
    """Loads mapping of old values to new values from CSV file."""
    try:
        path = Path(file_path)
        if not path.exists():
            logging.error(f"CSV file not found: '{file_path}'")
            sys.exit(1)

        # df = pd.read_excel(file_path, usecols=[old_col, new_col], engine='openpyxl')
        df = pd.read_csv(file_path, usecols=[old_col, new_col])


        if old_col not in df.columns or new_col not in df.columns:
            logging.error(f"Required columns '{old_col}' or '{new_col}' not found in CSV file '{file_path}'.")
            sys.exit(1)

        df.dropna(subset=[old_col], inplace=True)

        mapping = dict(zip(df[old_col].astype(str).str.strip(), df[new_col].astype(str).str.strip()))
        return mapping

    except ValueError as ve:
        logging.error(f"Error reading CSV file '{file_path}': {ve}")
        sys.exit(1)
    except Exception as e:
        logging.exception(f"Unexpected error while loading CSV mapping from '{file_path}': {e}")
        sys.exit(1)


def load_json(file_path: str) -> List[Dict[str, Any]]:
    """Loads JSON file and returns data."""
    try:
        path = Path(file_path)
        if not path.exists():
            logging.error(f"JSON file not found: '{file_path}'")
            sys.exit(1)

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            logging.error(f"Expected a JSON array (list of objects) in file: '{file_path}'")
            sys.exit(1)

        return data

    except json.JSONDecodeError as jde:
        logging.error(f"Invalid JSON format in '{file_path}': {jde}")
        sys.exit(1)
    except Exception as e:
        logging.exception(f"Unexpected error while loading JSON file '{file_path}': {e}")
        sys.exit(1)


def save_json(data: List[Dict[str, Any]], file_path: str):
    """Saves the updated data to a JSON file."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.exception(f"Failed to write updated JSON to '{file_path}': {e}")
        sys.exit(1)


def process_json_data(
    json_data: List[Dict[str, Any]],
    key_name: str,
    value_mapping: Dict[str, str]
) -> List[Dict[str, Any]]:
    """Updates or removes objects from JSON based on mapping rules."""
    updated_data = []
    skipped = 0

    for index, obj in enumerate(json_data):
        try:
            if not isinstance(obj, dict):
                logging.warning(f"Skipping invalid JSON object at index {index}: Not a dictionary.")
                skipped += 1
                continue

            if key_name not in obj:
                logging.warning(f"Key '{key_name}' not found in object at index {index}, skipping.")
                skipped += 1
                continue

            key_value = str(obj.get(key_name, "")).strip()
            new_value = value_mapping.get(key_value)

            if new_value and new_value.lower() != "nan":
                obj[key_name] = new_value
                updated_data.append(obj)
            else:
                skipped += 1

        except Exception as e:
            logging.warning(f"Error processing object at index {index}: {e}")
            skipped += 1

    logging.info(f"Total records skipped or removed: {skipped}")
    return updated_data


def parse_arguments():
    parser = argparse.ArgumentParser(description="Update JSON values based on CSV mapping.")
    parser.add_argument("--json_input_path", required=True, help="Path to input JSON file")
    parser.add_argument("--json_key_name", required=True, help="Key name in JSON to update")
    parser.add_argument("--json_output_path", required=True, help="Path to save updated JSON")
    parser.add_argument("--csv_path", required=True, help="Path to CSV file with mapping")
    parser.add_argument("--old_data_col_name", required=True, help="Column name for old data in CSV")
    parser.add_argument("--new_data_col_name", required=True, help="Column name for new data in CSV")
    return parser.parse_args()


def main():
    setup_logging()
    args = parse_arguments()

    logging.info("==== JSON Updater Started ====")
    logging.info(f"JSON input file       : {args.json_input_path}")
    logging.info(f"JSON key to update    : '{args.json_key_name}'")
    logging.info(f"CSV mapping file    : {args.csv_path}")
    logging.info(f"Old column in CSV   : '{args.old_data_col_name}'")
    logging.info(f"New column in CSV   : '{args.new_data_col_name}'")
    logging.info(f"JSON output file      : {args.json_output_path}")

    try:
        logging.info("Loading CSV mapping...")
        value_mapping = load_csv_mapping(args.csv_path, args.old_data_col_name, args.new_data_col_name)
        logging.info(f"Successfully loaded {len(value_mapping)} mappings from CSV.")

        logging.info("Loading JSON file...")
        json_data = load_json(args.json_input_path)
        logging.info(f"Successfully loaded {len(json_data)} records from JSON.")

        logging.info("Processing JSON data...")
        updated_data = process_json_data(json_data, args.json_key_name, value_mapping)
        logging.info(f"Retained {len(updated_data)} records after processing.")

        logging.info("Saving updated JSON file...")
        save_json(updated_data, args.json_output_path)
        logging.info(f"Updated JSON saved successfully to '{args.json_output_path}'")

        logging.info("==== JSON Updater Completed Successfully ====")

    except Exception as e:
        logging.exception(f"An unexpected error occurred during processing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
