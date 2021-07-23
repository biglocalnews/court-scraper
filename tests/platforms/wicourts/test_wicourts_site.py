from unittest.mock import call, patch

import pytest
from tests.conftest import CAPTCHA_API_KEY

from court_scraper.platforms.wicourts import WicourtsSite
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
    }
    results = site.search(court_scraper_dir, **kwargs)
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
    site = WicourtsSite(place_id)
    site = WicourtsSite(place_id, CAPTCHA_API_KEY)
    kwargs = {
        'start_date': start,
        'end_date': end,
        'headless': headless,
    }
    results = site.search(court_scraper_dir, **kwargs)
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
    }
    results = site.search(court_scraper_dir, **kwargs)
    assert len(results) == 2


def test_misconfigured_search(court_scraper_dir, headless):
    with pytest.raises(SearchConfigurationError):
        case_numbers=['2021CV003851','2021CV003850']
        place_id = 'wi_milwaukee'
        site = WicourtsSite(place_id, 'DUMMY_CAPTCHA_API_KEY')
        kwargs = {
            'headless': headless,
        }
        results = site.search(court_scraper_dir, **kwargs)

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
        'headless': headless,
    }
    results = site.search(court_scraper_dir, **kwargs)
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
        'headless': headless,
    }
    results = site.search(court_scraper_dir, **kwargs)
    assert len(results) == 2


