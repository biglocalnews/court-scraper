from unittest.mock import call, patch

import pytest

from court_scraper.platforms.wicourts import WicourtsSite

@pytest.fixture
def captcha_api_key():
    return "API KEY"


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
        'case_details': True,
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
        'case_details': True,
        'start_date': start,
        'end_date': end,
        'headless': headless,
    }
    results = site.search(court_scraper_dir, **kwargs)
    assert len(results) == 6

# TODO: test single case number search
# TODO: test case type support
# TODO: test multiple case number search

