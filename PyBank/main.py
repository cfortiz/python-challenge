import csv
import os
import sys
import logging


VERBOSE_LOGGING = True

DEFAULT_BUDGET_DATA_CSV_FILENAME = os.path.join("Resources", "budget_data.csv")
DEFAULT_REPORT_FILENAME = os.path.join("analysis", "budget_data_analysis.txt")

logger = logging.getLogger()


def main():
    success, failure = 0, -1
    
    exit_code = failure
    try:
        budget_data = import_budget_data()
        analysis = analyze_budget_data(budget_data)
        report = format_analysis(analysis)
        export_and_print_report(report)
        exit_code = success
    except Exception as e:
        exit_code = failure
        logger.exception(f"An unknown error was caught by main.")
    finally:
        return exit_code


def import_budget_data(filename=None):
    if filename is None:
        filename = DEFAULT_BUDGET_DATA_CSV_FILENAME
    
    logger.info(f"Importing budget data from {filename!r}")
    
    with open(filename, "r") as csv_file:
        reader = csv.reader(csv_file)
        
        headers = next(reader)
        logger.debug(f"{filename!r} had {headers=}")
        
        budget_data = list(reader)
    
        logger.debug(f"Found {len(budget_data)} data rows in {filename!r}")
    
    logger.info(f"Imported budget data from {filename!r}")
    
    return budget_data


def analyze_budget_data(budget_data):
    pass


def format_analysis(analysis):
    pass


def export_and_print_report(report, report_filename=None):
    pass


def init_logging(verbose=VERBOSE_LOGGING):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.WARNING)


if __name__ == "__main__":
    init_logging()    
    exit(main())
