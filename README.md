# python-challenge
Module 3 Challenge - Use the concepts you've learned to complete two Python
challenges, PyBank and PyPoll.

## Files

* `README.md`: This file
* `PyBank/main.py`: script that solves the PyBank challenge requirements
* `PyBank/Resources/budget_data.py`: CSV file with budget data (provided)
* `PyBank/analysis/budget_data_analysis.txt`: Budget analysis text report
* `PyPoll/main.py`: script that solves the PyBank challenge requirements
* `PyPoll/Resources/election_data.py`: CSV file with election data (provided)
* `PyPoll/analysis/election_data_analysis.txt`: Election analysis text report

## Instructions

**From the repo's base directory**, change directory to the specific challenge's
sub-directory, and run the `main.py` script with the python interpreter.

### PyBank
```
cd PyBank
python main.py
```

### PyPoll
```
cd PyPoll
python main.py
```

## Notes

### Dependencies and requirements

The code has no module dependencies outside the standard library and consists of
a single python script for each of the two challenges (see Modules section for
details).

Care should be taken to run the scripts with python 3.12 or later, since both
`PyBank/main.py` and `PyPoll/main.py` use new features for f-string literals
introduced in 3.12 which allow nesting the same type of quotation marks inside
interpolated expressions (see [PEP-701](https://peps.python.org/pep-0701/)
for details).

### Challenge Similarities and Differences

Both challenges require that we import data from a CSV file, analyze it,
prepare a report from that analysis, and finally export that report to a text
file and print it to standard output.

The two scripts mainly differ in how to analyze the data, and how to format the
analysis into a report, since both of those tasks are specific to each dataset's
problem domain and the challenge's specification.

### PyBank

PyBank wants us to compute summaries on the data provided.  It wants an overall
count of the number of months detailed in the data, as well as the total profit,
i.e. the sum of all profits as provided.  Note that for readability, simplicity,
and brevity, profit is used in the code interchangeably for profit and/or loss.

More importantly, it wants a first order forward difference between the profits
as the change in profits between periods, including the average change in
profits, as well as the period and profit change with the greatest increase and
decrease in profit change overall.  It was important to note that the number of
changes in profit is one less than the number of months.

### PyPoll

PyPoll wants us to compute some summaries on the data provided.  While it also
wants a count of all votes in the data, similar to PyBank wanting the count
of total number of months of data, it also wanted vote counts grouped by
candidate.

In order to do so, it was convenient to use the `defaultdict` data type from the
`collections` module in the standard library.  It is a `dict` subtype that
simplifies a typical use case.  From the official documentation:

> Setting the `default_factory` to `int` makes the `defaultdict` useful for
> counting (like a bag or multiset in other languages).

This allows us to count votes for each candidate without first having to check
if the candidate is in the `dict`, then adding the key with the initial value of
0 for that candidate's vote count **before** incrementing the count.  See Python
Docs: collections.defaultdict in references for details, especially the example
that counts occurrences of each letter in the string "mississippi".

## Modules

* `csv`: For `csv.reader` to load data from CSV files
* `os`: For `os.path.join` to determine file paths (filenames)
* `sys`: For `sys.stdout` to simplify export and print functions
* `collections`: For `collections.defaultdict` to compute grouped totals

## References

* [Python PEPs: PEP-701](https://peps.python.org/pep-0701/)
* [Python Docs: collections.defaultdict](https://docs.python.org/3/library/collections.html#collections.defaultdict)
