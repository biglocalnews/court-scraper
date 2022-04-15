"""Test date-based search for counties only covered by the
the general Search page, as opposed to the Daily Filings Search.

Tulsa is available via Daily Filings Search, whereas
Alfalfa and dozens of other smaller counties are only
available via general Search.
"""
import logging
from unittest import mock

import pytest

from court_scraper.platforms.oscn import Site as Oscn
from court_scraper.platforms.oscn.pages.search import Search


@pytest.mark.vcr()
def test_small_counties_date_search_basic():
    place_id = "ok_alfalfa"
    day = "2021-07-01"
    site = Oscn(place_id)
    results = site.search_by_date(start_date=day, end_date=day, case_details=False)
    # There should be a single date
    dates = {case.filing_date for case in results}
    assert len(dates) == 1
    assert dates == {day}
    cases = sorted(results, key=lambda case: case.number)
    # There should be four cases on this day
    assert len(cases) == 4
    first = results[0]
    # Check for presence of other expected data points
    assert first.place_id == place_id
    assert first.number == "CJ-2021-00008"
    assert first.filing_date == day
    expected_parties = [
        "BEISEL, JAMIE S (Plaintiff)",
        "BUCK, JAMES MELVIN (Plaintiff)",
        "BUCK, MARLENE SUE (Plaintiff)",
        "FIRETHORN HOLDINGS, LLC (Defendant)",
        "HADWIGER, KYLE (ATTORNEY)",
    ]
    assert first.parties == expected_parties
    # And the absence of case detail, since we didn't
    # request case_detail page to be scraped
    assert getattr(first, "judge", None) is None


@pytest.mark.vcr()
def test_small_counties_truncation_warning(caplog):
    # To test truncation, we need to directly use Search
    # rather than the higher-level Site class, because it's
    # difficult finding individual days that exceed 500 results
    # for smaller counties. So we'll use Tulsa here, although
    # under normal circumstances, Tulsa will default to the DailyFilings search
    caplog.set_level(logging.WARN)
    place_id = "ok_tulsa"
    day = "2021-07-01"
    search = Search(place_id)
    results = search.search(start_date=day, end_date=day, case_details=False)
    # Should warn user that results were truncated
    expected_warning = "WARNING: Results were truncated for your search."
    assert expected_warning in caplog.text
    # But still return case info
    assert len(results) == 171


@pytest.mark.vcr()
def test_small_counties_no_results():
    place_id = "ok_alfalfa"
    day = "2021-07-04"
    site = Oscn(place_id)
    results = site.search_by_date(start_date=day, end_date=day, case_details=False)
    assert len(results) == 0


@pytest.mark.vcr()
def test_small_counties_defaults_to_current_day():
    from court_scraper.platforms.oscn.site import Site as Oscn

    with mock.patch.object(Oscn, "current_day", "2021-07-01"):
        place_id = "ok_alfalfa"
        site = Oscn(place_id)
        results = site.search_by_date(case_details=False)
        dates = {case.filing_date for case in results}
        assert len(dates) == 1
        assert len(results) == 4


@pytest.mark.vcr()
def test_small_counties_multiple_day_results():
    place_id = "ok_alfalfa"
    start = "2021-07-01"
    end = "2021-07-02"
    site = Oscn(place_id)
    results = site.search_by_date(start_date=start, end_date=end, case_details=False)
    dates = {case.filing_date for case in results}
    assert dates == {start, end}
    assert len(results) == 10


@pytest.mark.vcr()
def test_small_counties_case_details():
    place_id = "ok_alfalfa"
    day = "2021-07-01"
    site = Oscn(place_id)
    # Here we set case_details to True to trigger detail page scraping
    results = site.search_by_date(start_date=day, end_date=day, case_details=True)
    # There should be a single entry for the searched date
    dates = {case.filing_date for case in results}
    assert len(dates) == 1
    first = sorted(results, key=lambda case: case.number)[0]
    # Check for presence of other expected data points
    assert first.filing_date == day
    assert first.place_id == place_id
    assert first.number == "CJ-2021-00008"
    # Case details should be available
    assert first.type == "Civil relief more than $10,000: MONEY JUDGMENT"
    assert first.judge == "ANGLE, LOREN E."
    assert first.close_date is None
