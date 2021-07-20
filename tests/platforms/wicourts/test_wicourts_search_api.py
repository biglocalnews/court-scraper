from court_scraper.platforms.wicourts.search_api import SearchApi

import pytest


@pytest.mark.vcr()
def test_api_search_by_filing_date():
    county = 'milwaukee'
    start, end = ['07-01-2021'] * 2
    api = SearchApi(county)
    cases = api.search_by_filing_date(start, end)
    # Returns CaseIno instances
    assert len(cases) == 346
    sorted_cases = sorted(cases, key=lambda case: case.number)
    first = sorted_cases[0]
    assert first.filing_date == '2021-07-01'
    assert first.number == '2019PA000978PJ'
    assert first.party == 'FLECHA, RICARDO N'
    assert first.caption == 'In Re the Paternity of K. S. F.'
    assert first.status == 'Closed'
    assert first.county == 'Milwaukee'
    assert first.county_num == 40


@pytest.mark.vcr()
def test_api_search_with_case_type():
    county = 'milwaukee'
    start, end = ['07-01-2021'] * 2
    params = {
        'caseType': 'CV,OL' # Civil and Other Liens
    }
    api = SearchApi(county)
    cases = api.search_by_filing_date(start, end, extra_params=params)
    assert len(cases) == 27
