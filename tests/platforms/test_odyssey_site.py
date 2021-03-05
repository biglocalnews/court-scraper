from unittest.mock import call, patch

import pytest

from court_scraper.platforms.odyssey_site import OdysseySite


@patch('court_scraper.platforms.odyssey_site.site.LoginPage')
@patch('court_scraper.base.selenium_site.webdriver')
def test_login(webdriver_mock, login_page_mock):
    site = OdysseySite(
        'http://somesite.com',
        'user',
        'pass',
        '/some_path/'
    )
    site.login()
    # Login initializes chrome driver
    assert webdriver_mock.Chrome.called
    # and calls login
    expected_calls = [
        call().go_to(),
        call().login()
    ]
    actual_calls = login_page_mock.mock_calls
    for expected in expected_calls:
        assert expected in actual_calls


@pytest.mark.parametrize(
    "test_input",
    [
        (
            "https://ody.dekalbcountyga.gov/portal/Home/Dashboard/29",
            ["19d89169"]
        ),
    ]
)
@pytest.mark.slow
@pytest.mark.webtest
def test_search(test_input, headless, live_configs, court_scraper_dir):
    auth = live_configs['ga_dekalb']
    username = auth['username']
    password = auth['password']
    url, case_ids = test_input
    site = OdysseySite(url, username, password, download_dir=court_scraper_dir)
    site.login(headless=headless)
    results = site.search(search_terms=case_ids, headless=False)
    assert len(results) == 1
