"""Test date-based search for counties only covered by the
the general Search page, as opposed to the Daily Filings Search.

Tulsa is available via Daily Filings Search, whereas
Alfalfa and dozens of other smaller counties are only
available via general Search.
"""
from pathlib import Path
from unittest import mock

import pytest

from court_scraper.platforms.oscn import Oscn


@pytest.mark.vcr()
def test_small_counties_date_search_basic():
    place_id = 'ok_alfalfa'
    day = '2021-07-01'
    site = Oscn(place_id)
    # Returns a SearchResults dict-like object
    results = site.search_by_date(start_date=day, end_date=day, case_details=False)
    # There should be a single entry for the searched date
    assert results.count_of_days == 1
    data = results[day]
    cases = sorted(data['cases'], key=lambda case: case.number)
    # There should only be four cases on this day
    assert len(cases) == 4
    # Raw html should be stored in the date's dict value (e.g. for caching)
    assert 'html' in data
    first = data['cases'][0]
    # Check for presence of other expected data points
    assert first.place_id == place_id
    assert first.number == 'CJ-2021-00008'
    expected_parties = [
        'BEISEL, JAMIE S (Plaintiff)',
        'BUCK, JAMES MELVIN (Plaintiff)',
        'BUCK, MARLENE SUE (Plaintiff)',
        'FIRETHORN HOLDINGS, LLC (Defendant)',
        'HADWIGER, KYLE (ATTORNEY)'
    ]
    assert first.parties == expected_parties
    # And the absence of case detail, since we didn't
    # request case_detail page to be scraped
    assert getattr(first, 'judge', None) is None


