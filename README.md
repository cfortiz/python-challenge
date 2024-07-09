# python-challenge
Module 3 Challenge - Use the concepts you've learned to complete two Python
challenges, PyBank and PyPoll.

## Overall notes

### Similarities

Both challenges require that we import data from a CSV file, analyze it,
prepare a report from that analysis, and finally export that report to a text
file and print it to standard output.

### Dependencies and requirements

The scripts have no third party module dependencies, but should be run with
python 3.12 or later, since they use new features for f-string literals which
allow nesting the same type of quotation marks inside interpolated expressions
(see [PEP-701](https://peps.python.org/pep-0701/) for details).

## PyBank

PyBank wants us to compute summaries on the data provided.  It wants an overall
count of the number of months detailed in the data, as well as the total profit,
i.e. the sum of all profits as provided.

More importantly, it wants a first order forward difference between the profits
as the change in profits between periods, including the average change in
profits, as well as the period and profit change with the greatest increase and
decrease in profit change overall.  It was important to note that the number of
changes in profit is one less than the number of months.

Finally, because some computations involved currency, it was important to use
the Decimal data type from the decimal module of the standard library.  Per the
official documentation:

> Decimal is based on a floating-point model which was designed with people in
> mind, and necessarily has a paramount guiding principle: computers must
> provide an arithmetic that works in the same way as the arithmetic that people
> learn at school. - _excerpt from the decimal arithmetic specification_
(see References below).

### Instructions

From the main repo directory, change directory to `PyBank`, then run the
`main.py` script.

```
cd PyBank
python main.py
```

### Files

* `PyBank/main.py`: script that solves the PyBank challenge requirements
* `PyBank/Resources/budget_data.py`: CSV file with budget data (provided)
* `PyBank/analysis/budget_data_analysis.txt`: Text report of analysis results.

## PyPoll

PyPoll wants us to compute some summaries on the data provided.  While it also
wants a count of all votes in the data, similar to PyBank wanting the count
of total number of months of data, it also wanted vote counts grouped by
candidate.

In order to do so, it was convenient to use the defaultdict data type from the
collections module in the standard library.  That type is a dict subtype that
simplifies a typical use case: where we want access to a key in the dict to
default to a value determined by some constructor function.  For example, this
allows us to default the value associated with a key to the int 0, so that we
can automatically increment it without first having to manually add the value
for that key each time.  This allows us to count votes for each candidate
without first having to check if the candidate is in the dict, and then adding
the key with the initial value of 0 for that candidate's vote count **before**
incrementing the count.

The actual report generation (analysis formatting) was simpler in this case,
since there were fewer fields that required special consideration.

### Instructions

From the main repo directory, change directory to `PyPoll`, then run the
`main.py` script.

```
cd PyPoll
python main.py
```

### Files

* `PyPoll/main.py`: script that solves the PyBank challenge requirements
* `PyPoll/Resources/election_data.py`: CSV file with election data (provided)
* `PyPoll/analysis/election_data_analysis.txt`: Text report of analysis results.

## References

* [Python PEPs: PEP-701](https://peps.python.org/pep-0701/)
* [Python Docs: decimal.Decimal](https://docs.python.org/3/library/decimal.html)
* [Python Docs: collections.defaultdict](https://docs.python.org/3/library/collections.html#collections.defaultdict)
