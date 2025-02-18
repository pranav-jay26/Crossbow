#!/usr/bin/env python3

import argparse
import crossbow as cxb
import pyarrow as pa
import pandas as pd
import os
import sys
import logging
from typing import Optional, List

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

SUPPORTED_EXCEL_EXTENSIONS = ('.xlsx', '.xls', '.ods')

def select_excel_file() -> Optional[str]:
    """
    Interactive selection of Excel files in the current directory with error handling.
    
    Returns:
        Optional[str]: Path to selected Excel file or None if no valid selection
    """
    try:
        xlsx_files = [
            f for f in os.listdir(os.getcwd()) 
            if f.lower().endswith(SUPPORTED_EXCEL_EXTENSIONS)
        ]

        if not xlsx_files:
            logger.warning("No Excel files found in current directory.")
            return None

        logger.info("Found %d Excel files:", len(xlsx_files))
        for i, file_name in enumerate(xlsx_files, 1):
            print(f"{i}. {file_name}")

        while True:
            try:
                choice = int(input("\nEnter file number (0 to cancel): "))
                if choice == 0:
                    logger.info("File selection cancelled.")
                    return None
                if 1 <= choice <= len(xlsx_files):
                    selected_file = xlsx_files[choice - 1]
                    logger.info("Selected file: %s", selected_file)
                    return selected_file
                logger.warning("Invalid choice. Please enter a number between 1 and %d.", len(xlsx_files))
            except ValueError:
                logger.warning("Invalid input. Please enter a numeric value.")

    except Exception as e:
        logger.error("Error selecting Excel file: %s", str(e), exc_info=True)
        return None

def get_sheet_names(file_path: str) -> List[str]:
    """
    Get list of sheet names from an Excel file using crossbow's Rust implementation.
    
    Args:
        file_path (str): Path to Excel file
        
    Returns:
        List[str]: List of sheet names
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        # Get sheets using crossbow's internal implementation
        workbook = cxb._get_workbook(file_path)  # Assuming exposed Rust method
        return workbook.sheet_names()
        
    except Exception as e:
        logger.error("Error retrieving sheet names: %s", str(e), exc_info=True)
        return []

def main():
    """Main CLI entry point for crossbow Python interface."""
    parser = argparse.ArgumentParser(
        description="Crossbow: High-performance Excel/CSV to Arrow converter",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-f', '--file', 
        help="Path to input file (Excel or CSV)",
        type=str,
        required=False
    )
    parser.add_argument(
        '-s', '--sheet',
        help="Sheet name (for Excel files)",
        type=str,
        required=False
    )
    parser.add_argument(
        '-v', '--verbose',
        help="Enable verbose logging",
        action='store_true'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        
    try:
        # File selection logic
        file_path = args.file
        if not file_path:
            file_path = select_excel_file()
            if not file_path:
                logger.info("No file selected. Exiting.")
                return
                
        # Sheet selection logic
        sheet_name = args.sheet
        if file_path.lower().endswith(SUPPORTED_EXCEL_EXTENSIONS) and not sheet_name:
            sheets = get_sheet_names(file_path)
            if sheets:
                logger.info("Available sheets:")
                for i, sheet in enumerate(sheets, 1):
                    print(f"{i}. {sheet}")
                sheet_choice = int(input("\nEnter sheet number: "))
                sheet_name = sheets[sheet_choice - 1]
                
        # Data processing
        if file_path.lower().endswith(SUPPORTED_EXCEL_EXTENSIONS):
            logger.info("Reading Excel file: %s (Sheet: %s)", file_path, sheet_name)
            batch = cxb.read_excel_py(file_path, sheet_name)
        else:
            logger.info("Reading CSV file: %s", file_path)
            batch = cxb.read_csv_py(file_path)
            
        table = pa.Table.from_batches([batch])
        df = table.to_pandas()
        
        logger.info("Successfully loaded data:\n%s", df.head())
        
    except Exception as e:
        logger.error("Fatal error processing file: %s", str(e), exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
