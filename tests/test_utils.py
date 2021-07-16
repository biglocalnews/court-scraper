from datetime import datetime

import pytest

from court_scraper.utils import dates_for_range



@pytest.mark.parametrize(
    "start,end,kwargs,expected", [
        # Single day
        (
            '2021-07-05', '2021-07-05', {},
            [datetime(2021, 7, 5)]
        ),
        # Multiple days
        (
            '2021-07-05', '2021-07-06', {},
            [datetime(2021, 7, 5), datetime(2021, 7, 6)]
        ),
        # Formatted output
        (
            '2021-07-05', '2021-07-06', {'output_format': "%m-%d-%y"},
            ["07-05-21", "07-06-21"]
        ),
        # Custom input format and output format
        (
            '07-05-21', '07-06-21', {'input_format': "%m-%d-%y", 'output_format': "%Y-%m-%d"},
            ["2021-07-05", "2021-07-06"]
        ),
    ],
)
def test_dates_for_range(start, end, kwargs, expected):
    dates = dates_for_range(start, end, **kwargs)
    assert dates == expected
