import pytest

from court_scraper.platforms.wicourts import WicourtsSite


@pytest.mark.slow
@pytest.mark.webtest
def test_search_by_date_case_details(court_scraper_dir):
    # Forest "2021-06-30" has 2 cases
    # Adams  "2021-06-16" has 4 cases
    # Milwaukee "2021-07-31" has 346 cases!
    day = "2021-06-30"
    # Test with a smaller county
    place_id = "wi_forest" #wi_milwaukee"
    site = WicourtsSite(place_id)
    kwargs = {
        'case_details': True,
        'start_date': day,
        'end_date': day,
        'headless': True,
    }
    results = site.search(court_scraper_dir, **kwargs)
    assert len(results) == 2

