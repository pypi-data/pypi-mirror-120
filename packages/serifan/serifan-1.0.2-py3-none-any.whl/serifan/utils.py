"""
Utils module.

This module provides the following functions:

- list_strings_to_dates()
"""
from datetime import date
from datetime import datetime as dt
from typing import List


def list_strings_to_dates(lst) -> List[date]:
    """
    Convert a list of date strings to a list of date objects.

    :param lst: A list of date strings
    :type params: list of str

    :return: A list of `datetime.date` objects
    :rtype: date
    """
    # One of the string dates in the api has a period at the end.
    return [dt.strptime(d.strip("."), "%Y-%m-%d").date() for d in lst["dates"]]
