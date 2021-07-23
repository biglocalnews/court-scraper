from unittest.mock import call, patch

import pytest

from court_scraper.platforms.wicourts import WicourtsSite

@pytest.fixture
def captcha_api_key():
    # TODO: Look up API using same strategy as captcha decorator
    return 'YOUR API KEY'


@pytest.mark.slow
@pytest.mark.webtest
def test_search_with_case_details(court_scraper_dir, captcha_api_key, headless):
    # Forest "2021-06-30" has 2 cases
    # Adams  "2021-06-16" has 4 cases
    # Milwaukee "2021-07-31" has 346 cases!
    day = "2021-06-30"
    # Test with a smaller county
    place_id = "wi_forest" #wi_milwaukee"
    site = WicourtsSite(place_id, captcha_api_key)
    kwargs = {
        'start_date': day,
        'end_date': day,
        'headless': headless,
    }
    results = site.search(court_scraper_dir, **kwargs)
    assert len(results) == 2


@pytest.mark.slow
@pytest.mark.webtest
def test_search_multiple_days_with_details(court_scraper_dir, captcha_api_key, headless):
    # Forest "2021-06-24" has 2 cases
    # Forest "2021-06-23" has 4 cases
    start = "2021-06-23"
    end = "2021-06-24"
    # Test with a smaller county
    place_id = "wi_forest" #wi_milwaukee"
    site = WicourtsSite(place_id)
    site = WicourtsSite(place_id, captcha_api_key)
    kwargs = {
        'start_date': start,
        'end_date': end,
        'headless': headless,
    }
    results = site.search(court_scraper_dir, **kwargs)
    assert len(results) == 6


@pytest.mark.slow
@pytest.mark.webtest
def test_case_number_search(court_scraper_dir, captcha_api_key, headless):
    case_numbers=['2021CV003851','2021CV003850']
    place_id = 'wi_milwaukee'
    site = WicourtsSite(place_id, captcha_api_key)
    kwargs = {
        'headless': headless,
        'case_numbers': case_numbers,
    }
    results = site.search(court_scraper_dir, **kwargs)
    assert len(results) == 2

