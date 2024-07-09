# Module 3 PyBank Challenge
"""Script to import budget data, analyze it, and report the formatted analysis

Imports the budget data from a csv file.  Then it analyzes the data, computing
some summary information such as the total number of months of budget data,
the total profit for the entire period, the average month-to-month change in
profits, and the month and change for the greatest increase and decrease in
profit changes.

"""
import csv
import os
import sys
import logging
from decimal import Decimal  # Currency should be Decimal to avoid roundoff err


# Logging setup constants
VERBOSE_LOGGING = True  # Set to True to enable verbose logging
QUIET_LOGGING = True  # Set to True to disable logging
VERBOSE_LOGGING_LEVEL = logging.INFO
# VERBOSE_LEVEL = logging.DEBUG
DEFAULT_LOGGING_LEVEL = logging.WARNING

# Default filenames
DEFAULT_BUDGET_DATA_CSV_FILENAME = os.path.join("Resources", "budget_data.csv")
DEFAULT_REPORT_FILENAME = os.path.join("analysis", "budget_data_analysis.txt")

# Create a logger for the script
logger = logging.getLogger()


def main():
    """Entry point for script.
    
    While handling potential errors, it imports budget data, analyzes the data,
    formats the analysis into a report, and then exports and prints the report.
    
    If an error occurs (an exception is raised) and it hasn't been handled
    elsewhere, it will catch it and set the exit code to a failure condition.
    Additionally, if logging isn't quieted, it will log the error to stderr,
    including a stack trace.
    
    """
    success, failure = 0, -1
    
    exit_code = failure
    try:
        budget_data = import_budget_data()
        analysis = analyze_budget_data(budget_data)
        report = format_analysis_report(analysis)
        export_and_print_report(report)
        exit_code = success
    except Exception as e:
        exit_code = failure
        logger.exception(f"An unknown error was caught by main.")
    finally:
        return exit_code


def import_budget_data(filename=None):
    """Imports budget data from a csv file.
    
    Args:
        filename (str): path of the csv file to import (default in 
            DEFAULT_BUDGET_DATA_CSV_FILENAME)
    
    Returns:
        A list of lists of strings.  Each inner list contains a string for the
        month-year combined date, and a string for the profit (or loss) value
        in that order.
        
    """
    # Handle default filename
    if filename is None:
        filename = DEFAULT_BUDGET_DATA_CSV_FILENAME
    
    logger.info(f"Importing budget data from {filename!r}")
    
    # Open and read the csv file, discarding the header
    with open(filename, "r") as csv_file:
        reader = csv.reader(csv_file)
        
        headers = next(reader)
        logger.debug(f"{filename!r} had {headers=}")
        
        budget_data = list(reader)
    
        logger.debug(f"Found {len(budget_data)} data rows in {filename!r}")
    
    logger.info(f"Imported budget data from {filename!r}")
    
    return budget_data


def analyze_budget_data(budget_data):
    """Analyzes the budget data, computing several summary totals.
    
    Args:
        budget_data (list[list[str]]): budget data rows, each row has first a
            combination of the month-year date of the period, and second the
            profit or loss value for that period
    
    Returns:
        A dict with the string summary name as the key, and the actual summary
        as the value.
        
    """
    logger.info("Analyzing budget data")
    
    # Initialize totals
    total_months = len(budget_data)
    total_changes = total_months - 1  # One fewer changes than months
    total_profit = Decimal("0.00")
    total_change = Decimal("0.00")
    
    # No profits yet, so no last_profit
    last_profit = None
    change = None
    
    # Initialize greatest increase and decrease to None
    greatest_increase = None
    greatest_decrease = None
    
    for month, profit in budget_data:
        # Convert profit str into Decimal for calculations
        profit = Decimal(profit)
        
        # Accumulate profit to total
        total_profit += profit
        
        # Compute profit change, and accumulate total change
        if last_profit is not None:
            change = profit - last_profit
            total_change += change
        
        # Compute greatest increase and decrease
        if change is not None:
            if greatest_increase is None or greatest_increase[1] < change:
                greatest_increase = (month, change)
            if greatest_decrease is None or greatest_decrease[1] > change:
                greatest_decrease = (month, change)
        
        # Save profit as last_profit for change computations
        last_profit = profit
    
    # Consolidate the analysis
    analysis = dict(
        total_months=total_months,
        total=total_profit,
        average_change=total_change/total_changes,
        greatest_increase=greatest_increase,
        greatest_decrease=greatest_decrease,        
    )
    
    logger.debug(f"{analysis=}")
    
    logger.info("Analyzed budget data")
    
    return analysis


def format_analysis_report(analysis):
    """Format the analysis into a ready to print report.
    
    Args:
        analysis (dict[str, str|Decimal]): a mapping of summary names to
            summary values, including total_months, total (profit),
            average_change (in profits), greatest_increase (profit change),
            and greatest_decrease (in profits).
    
    Returns:
        A formatted report as a string.
        
    """
    logger.info("Formatting analysis report")

    # Convert analysis values into strings, rounding where appropriate
    total_months = f"{analysis["total_months"]}"
    total = f"${round(analysis["total"], 0)}"
    average_change = f"${round(analysis["average_change"], 2)}"
    increase_month, increase_profit = analysis["greatest_increase"]
    decrease_month, decrease_profit = analysis["greatest_decrease"]
    increase_profit = f"${round(increase_profit, 0)}"
    decrease_profit = f"${round(decrease_profit, 0)}"
    
    # Format greatest increase and decrease data
    increase = f"{increase_month} ({increase_profit})"
    decrease = f"{decrease_month} ({decrease_profit})"
    
    # Prepare report lines
    report_heading_lines = (
        f"Financial Analysis",  # Report title
        "-"*28,  # Horizontal separator (example was 28 chars wide)
    )    
    report_field_names = (
        "Total Months",
        "Total",
        "Average Change",
        "Greatest Increase in Profits",
        "Greatest Decrease in Profits",
    )    
    report_field_values = (
        total_months,
        total,
        average_change,
        increase,
        decrease,
    )
    report_field_lines = tuple(
        f"{name}: {value}"
        for name, value in zip(report_field_names, report_field_values)
    )

    # Join heading and field lines into report
    report = "\n".join(report_heading_lines + report_field_lines)

    logger.debug(f"Report:\n{report}")

    logger.info("Formatted analysis report")
    
    return report


def export_and_print_report(report, report_filename=None):
    """Exports the report to a text file, and prints it to stdout.
    
    Args:
        report (str): A formatted report.
        report_filename (str|None): The str filename for the export text file.
            If None, it will default to the constant DEFAULT_REPORT_FILENAME.
    
    """
    if report_filename is None:
        report_filename = DEFAULT_REPORT_FILENAME

    logger.info("Exporting and printing report")
    
    with open(report_filename, "w", encoding="utf-8") as report_file:
        for file in (report_file, sys.stdout):
            print(report, file=file)
    
    logger.info("Exported and printed report")


def init_logging(verbose=VERBOSE_LOGGING, quiet=QUIET_LOGGING):
    """Initializes logging used for debugging during development.
    
    Args:
        verbose (bool): Enables verbose logging (default VERBOSE_LOGGING)
        quiet (bool): Disables logging altogether (default QUIET_LOGGING)
        
    """
    if quiet:
        logger.addHandler(logging.NullHandler())
        logger.warning("This should never get logged")
    elif verbose:
        logging.basicConfig(level=VERBOSE_LOGGING_LEVEL)
    else:
        logging.basicConfig(level=logging.WARNING)


if __name__ == "__main__":
    init_logging()    
    exit(main())
