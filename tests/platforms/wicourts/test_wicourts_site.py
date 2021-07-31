from unittest.mock import call, patch

import pytest
from tests.conftest import CAPTCHA_API_KEY

from court_scraper.platforms.wicourts import Site as WicourtsSite
from court_scraper.platforms.wicourts.site import SearchConfigurationError



skip_test_reason = "You must configure captcha_service_api_key in ~/.court-scraper/config.yaml"


@pytest.mark.slow
@pytest.mark.webtest
@pytest.mark.skipif(CAPTCHA_API_KEY is None, reason=skip_test_reason)
def test_search_with_case_details(court_scraper_dir, headless):
    # Forest "2021-06-30" has 2 cases
    # Adams  "2021-06-16" has 4 cases
    # Milwaukee "2021-07-31" has 346 cases!
    day = "2021-06-30"
    # Test with a smaller county
    place_id = "wi_forest" #wi_milwaukee"
    site = WicourtsSite(place_id, CAPTCHA_API_KEY)
    kwargs = {
        'start_date': day,
        'end_date': day,
        'headless': headless,
        'download_dir': court_scraper_dir,
    }
    results = site.search(**kwargs)
    assert len(results) == 2


@pytest.mark.slow
@pytest.mark.webtest
@pytest.mark.skipif(CAPTCHA_API_KEY is None, reason=skip_test_reason)
def test_search_multiple_days_with_details(court_scraper_dir, headless):
    # Forest "2021-06-24" has 2 cases
    # Forest "2021-06-23" has 4 cases
    start = "2021-06-23"
    end = "2021-06-24"
    # Test with a smaller county
    place_id = "wi_forest" #wi_milwaukee"
    site = WicourtsSite(place_id, CAPTCHA_API_KEY)
    kwargs = {
        'start_date': start,
        'end_date': end,
        'headless': headless,
        'download_dir': court_scraper_dir,
    }
    results = site.search(**kwargs)
    assert len(results) == 6


@pytest.mark.slow
@pytest.mark.webtest
@pytest.mark.skipif(CAPTCHA_API_KEY is None, reason=skip_test_reason)
def test_case_number_search(court_scraper_dir, headless):
    case_numbers=['2021CV003851','2021CV003850']
    place_id = 'wi_milwaukee'
    site = WicourtsSite(place_id, CAPTCHA_API_KEY)
    kwargs = {
        'headless': headless,
        'case_numbers': case_numbers,
        'download_dir': court_scraper_dir,
    }
    results = site.search(**kwargs)
    assert len(results) == 2


def test_misconfigured_search(court_scraper_dir, headless):
    with pytest.raises(SearchConfigurationError):
        case_numbers=['2021CV003851','2021CV003850']
        place_id = 'wi_milwaukee'
        site = WicourtsSite(place_id, 'DUMMY_CAPTCHA_API_KEY')
        kwargs = {
            'headless': headless,
            'download_dir': court_scraper_dir,
        }
        results = site.search(**kwargs)

@pytest.mark.slow
@pytest.mark.webtest
@pytest.mark.skipif(CAPTCHA_API_KEY is None, reason=skip_test_reason)
def test_search_with_multiple_case_types_multiple_results(court_scraper_dir, headless):
    # Forest "2021-07-01" has 4 cases with 3 case types (TR, SC, FO)
    day = "2021-07-01"
    place_id = "wi_forest"
    site = WicourtsSite(place_id, CAPTCHA_API_KEY)
    kwargs = {
        'start_date': day,
        'end_date': day,
        'case_types': ['SC', 'TR'],
        'download_dir': court_scraper_dir,
        'headless': headless,
    }
    results = site.search(**kwargs)
    assert len(results) == 3

@pytest.mark.slow
@pytest.mark.webtest
@pytest.mark.skipif(CAPTCHA_API_KEY is None, reason=skip_test_reason)
def test_search_with_single_case_type_multiple_results(court_scraper_dir, headless):
    # Forest "2021-07-01" has 4 cases with 3 case types (TR, SC, FO)
    # Two of them are TRs
    day = "2021-07-01"
    place_id = "wi_forest"
    site = WicourtsSite(place_id, CAPTCHA_API_KEY)
    kwargs = {
        'start_date': day,
        'end_date': day,
        'case_types': ['TR'],
        'download_dir': court_scraper_dir,
        'headless': headless,
    }
    results = site.search(**kwargs)
    assert len(results) == 2


@pytest.mark.slow
@pytest.mark.webtest
@pytest.mark.skipif(CAPTCHA_API_KEY is None, reason=skip_test_reason)
def test_search_case_type_single_result(court_scraper_dir, headless):
    # Forest "2021-07-01" has 4 cases with 3 case types (TR, SC, FO)
    # One of them are is SC
    # Searches with single results redirect straight to case detail page
    day = "2021-07-01"
    place_id = "wi_forest"
    site = WicourtsSite(place_id, CAPTCHA_API_KEY)
    kwargs = {
        'start_date': day,
        'end_date': day,
        'case_types': ['SC'],
        'download_dir': court_scraper_dir,
        'headless': headless,
    }
    results = site.search(**kwargs)
    assert len(results) == 1


@pytest.mark.slow
@pytest.mark.webtest
def test_search_no_results(court_scraper_dir, headless):
    day = "2021-06-27" # Sunday
    place_id = "wi_forest"
    site = WicourtsSite(place_id, 'DUMMY_CAPTCHA_API_KEY')
    kwargs = {
        'start_date': day,
        'end_date': day,
        'download_dir': court_scraper_dir,
        'headless': headless,
    }
    results = site.search(**kwargs)
    assert len(results) == 0


@pytest.mark.slow
@pytest.mark.webtest
@pytest.mark.skipif(CAPTCHA_API_KEY is None, reason=skip_test_reason)
def test_multiname_county_date_search(court_scraper_dir, headless):
    day = "2021-06-22"
    place_id = "wi_green_lake"
    site = WicourtsSite(place_id, CAPTCHA_API_KEY)
    kwargs = {
        'start_date': day,
        'end_date': day,
        'download_dir': court_scraper_dir,
        'headless': headless,
    }
    results = site.search(**kwargs)
    assert len(results) == 5


@pytest.mark.slow
@pytest.mark.webtest
@pytest.mark.skipif(CAPTCHA_API_KEY is None, reason=skip_test_reason)
def test_multiname_county_case_number(court_scraper_dir, headless):
    place_id = "wi_green_lake"
    site = WicourtsSite(place_id, CAPTCHA_API_KEY)
    kwargs = {
        'case_numbers': ['2021CV000055'],
        'download_dir': court_scraper_dir,
        'headless': headless,
    }
    results = site.search(**kwargs)
    assert len(results) == 1


@pytest.mark.vcr()
def test_date_search_basic():
    "should provide metadata-only search that uses requests and provides more limited data points"
    # There are 4 cases total, 2 of them TRaffic
    day = "2021-07-01"
    place_id = "wi_forest"
    site = WicourtsSite(place_id, CAPTCHA_API_KEY)
    # case_details defaults to False
    kwargs = {
        'start_date': day,
        'end_date': day,
        'case_types': ['TR'],
    }
    results = site.search_by_date(**kwargs)
    assert len(results) == 2
    for case in results:
        assert case.filing_date == '2021-07-01'
        assert case.county == 'Forest'
        assert 'TR' in case.number


@pytest.mark.slow()
@pytest.mark.webtest()
def test_date_search_with_details(court_scraper_dir, headless):
    "should provide case details search that uses selenium"
    # There are 4 cases total, 2 of them TRaffic
    day = "2021-07-01"
    place_id = "wi_forest"
    site = WicourtsSite(place_id, CAPTCHA_API_KEY)
    kwargs = {
        'start_date': day,
        'end_date': day,
        'case_types': ['TR'],
        'case_details': True,
        'download_dir': court_scraper_dir,
        'headless': headless
    }
    results = site.search_by_date(**kwargs)
    assert len(results) == 2
    for case in results:
        assert case.filing_date == '2021-07-01'
        assert case.county == 'Forest'
        assert 'TR' in case.number
        # Check for some data points that are only found in detailed data
        assert case.type_code == 'TR'
        assert hasattr(case, 'parties') == True


@pytest.mark.slow()
@pytest.mark.webtest()
def test_date_search_details_multiday(court_scraper_dir, headless):
    # Forest "2021-06-24" has 2 cases
    # Forest "2021-06-23" has 4 cases
    start = "2021-06-23"
    end = "2021-06-24"
    place_id = "wi_forest"
    site = WicourtsSite(place_id, CAPTCHA_API_KEY)
    kwargs = {
        'start_date': start,
        'end_date': end,
        'case_details': True,
        'download_dir': court_scraper_dir,
        'headless': headless
    }
    results = site.search_by_date(**kwargs)
    assert len(results) == 6
