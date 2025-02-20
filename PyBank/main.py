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


# Default filenames
CSV_DATA_FILENAME = os.path.join("Resources", "budget_data.csv")
TXT_REPORT_FILENAME = os.path.join("analysis", "budget_data_analysis.txt")


def main():
    """Entry point for script.
    
    It imports budget data, analyzes the data, formats the analysis into a
    report, and then exports and prints the report.
    
    """
    budget_data = import_budget_data()
    analysis = analyze_budget_data(budget_data)
    report = format_analysis_report(analysis)
    export_and_print_report(report)


def import_budget_data(filename=None):
    """Imports budget data from a csv file.
    
    Args:
        filename (str): path of the csv file to import (default in 
            CSV_DATA_FILENAME)
    
    Returns:
        A list of lists of strings.  Each inner list contains a string for the
        month-year combined date, and a string for the profit (or loss) value
        in that order.
        
    """
    # Handle default filename
    if filename is None:
        filename = CSV_DATA_FILENAME
    
    # Open and read the csv file, discarding the header
    with open(filename, "r") as csv_file:
        reader = csv.reader(csv_file)
        headers = next(reader)  # csv data header, loaded but discarded
        budget_data = list(reader)
    
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
    # Initialize totals
    total_months = len(budget_data)
    total_changes = total_months - 1  # One fewer changes than months
    total_profit = 0
    total_change = 0
    
    # No profits yet, so no last_profit
    last_profit = None
    change = None
    
    # Initialize greatest increase and decrease to None
    greatest_increase = None
    greatest_decrease = None
    
    for month, profit in budget_data:
        # Convert profit str to int for calculations
        profit = int(profit)
        
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
    
    return analysis


def format_analysis_report(analysis):
    """Format the analysis into a ready to print report.
    
    Args:
        analysis (dict[str, object]): a mapping of summary names to
            summary values, including total_months, total (profit),
            average_change (in profits), greatest_increase (profit change),
            and greatest_decrease (in profits).
    
    Returns:
        A formatted report as a string.
        
    """
    # Convert analysis values into strings, rounding where appropriate
    total_months = f"{analysis["total_months"]}"
    total = f"${round(analysis["total"], 0)}"
    average_change = f"${round(analysis["average_change"], 2)}"
    increase_month, increase_profit = analysis["greatest_increase"]
    decrease_month, decrease_profit = analysis["greatest_decrease"]
    increase_profit = f"${increase_profit}"
    decrease_profit = f"${decrease_profit}"
    
    # Format greatest increase and decrease data
    increase = f"{increase_month} ({increase_profit})"
    decrease = f"{decrease_month} ({decrease_profit})"
    
    # Prepare report lines
    report_lines = (
        "Financial Analysis",  # title
        "-"*28, # horizontal bar (example was 28 chars wide)
        f"Total Months: {total_months}",
        f"Total: {total}",
        f"Average Change: {average_change}",
        f"Greatest Increase in Profits: {increase}",
        f"Greatest Decrease in Profits: {decrease}",
    )    

    # Join heading and field lines into report
    report = "\n".join(report_lines)

    return report


def export_and_print_report(report, report_filename=None):
    """Exports the report to a text file, and prints it to stdout.
    
    Args:
        report (str): A formatted report.
        report_filename (str|None): The str filename for the export text file.
            If None, it will default to the constant TXT_REPORT_FILENAME.
    
    """
    if report_filename is None:
        report_filename = TXT_REPORT_FILENAME

    with open(report_filename, "w", encoding="utf-8") as report_file:
        for file in (report_file, sys.stdout):
            print(report, file=file)


if __name__ == "__main__":
    main()
