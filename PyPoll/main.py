# Module 3 PyPoll Challenge
"""Script to import election data, analyze it, and report the formatted analysis

Imports the election data from a csv file.  Then it analyzes the data, computing
some summary information such as the total number of votes, the name, vote
count, and vote percentage for each candidate, and the winner of the election
by populat vote.  It then formats the analysis into a report, exports it to a
text file, and prints it to standard output.

"""
import csv
import os
import sys
from collections import defaultdict


# Default filenames
CSV_DATA_FILENAME = os.path.join("Resources", "election_data.csv")
TXT_REPORT_FILENAME = os.path.join("analysis", "election_data_analysis.txt")


def main():
    """Entry point for script.
    
    Imports election data, analyzes the data, formats the analysis into a
    report, and then exports and prints the report.
    
    """
    election_data = import_election_data()
    analysis = analyze_election_data(election_data)
    report = format_analysis_report(analysis)
    export_and_print_report(report)


def import_election_data(filename=None):
    """Imports election data from a csv file.
    
    Args:
        filename (str): path of the csv file to import (default in 
            CSV_DATA_FILENAME)
    
    Returns:
        A list of lists of strings.  Each inner list contains strings for the
        ballot-id, county, and candidate name in that order.
        
    """
    if filename is None:
        filename = CSV_DATA_FILENAME
    
    with open(filename, "r") as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)  # csv data header, loaded but discarded
        election_data = list(reader)
    
    return election_data


def analyze_election_data(election_data):
    """Analyzes the election data, computing several summary totals.
    
    Args:
        election_data (list[list[str]]): election data rows, each row has 3
            strings, the ballot_id, county, and candidate, in that order.
    
    Returns:
        A dict with the string summary name as the key, and the actual summary
        as the value.  The summaries are the total_votes, candidate_votes, and
        winner.  The total_votes is an integer count of all votes in the
        election.  The candidate_votes is a list of tuples, each with the
        candidate's name string, the integer count of votes for that candidate,
        and the percentage of votes for that candidate as a float.
        
    """
    total_votes = len(election_data)
    candidate_votes = defaultdict(int)  # See note below.
    winner = None
    
    # Note: defaultdict is a standard library subtype of dict from the
    # collections module.  It takes a constructor function as the first argument
    # to its constructor.  Whenever a value for a given key is first accessed,
    # it first assigns the result of calling that function.  It is useful for
    # cases such as these, where we are grouping totals under some category,
    # such as numer of votes received by a candidate.

    # Count each candidate's votes.
    for row in election_data:
        ballot_id, county, candidate = row  # Uses unpacking to get row values
        candidate_votes[candidate] += 1  # Increments candidate's votes
    
    # Determine the winner by populat vote.
    for candidate, votes in candidate_votes.items():
        if winner is None or votes > winner[1]:
            winner = (candidate, votes)
    
    # Gather the analysis
    analysis = dict(
        total_votes=total_votes,
        candidate_votes=[
            (candidate, votes, votes*100/total_votes)
            for candidate, votes
            in candidate_votes.items()
        ],
        winner=winner[0],
    )
    
    return analysis


def format_analysis_report(analysis):
    """Format the analysis into a ready to print report.
    
    Args:
        analysis (dict[str, object]): a mapping of summary names to summary
            values, including total_votes, candidate_votes, and winner.
    
    Returns:
        A formatted report as a string.
        
    """
    
    # Prepare a horizontal bar as a string
    horizontal_bar = "-"*25
    
    # The title of the report
    title = "Election Results"
    
    # Format the lines with actual summary data
    total_votes = f"Total Votes: {analysis["total_votes"]}"
    candidates = [
        f"{name}: {percentage:2.3f}% ({votes})"
        for name, votes, percentage in analysis["candidate_votes"]
    ]
    winner = f"Winner: {analysis["winner"]}"

    # Assemble the lines of the report in order
    report_lines = [
        title,
        horizontal_bar,
        total_votes,
        horizontal_bar,
        *candidates,  # *candidates inserts each str in candidates in order
        horizontal_bar,
        winner,
        horizontal_bar,
    ]

    # Join the report lines into the final report
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
