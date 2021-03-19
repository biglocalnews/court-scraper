from unittest.mock import call, patch

import pytest

from court_scraper.platforms.odyssey_site import OdysseySite


@patch('court_scraper.platforms.odyssey_site.site.LoginPage')
@patch('court_scraper.base.selenium_site.webdriver')
def test_login(webdriver_mock, login_page_mock):
    site = OdysseySite('http://somesite.com', '/tmp/some_path/')
    # Web driver instantiated during Site class initialization
    assert webdriver_mock.Chrome.called
    # Login requires password
    site.login('user', 'pass')
    # login method goes to login page and submits user creds
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
            "https://cmsportal.chathamcounty.org/Portal/Home/Dashboard/29",
            ["MGCV20-00001"]
        ),
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
    site = OdysseySite(url, download_dir=court_scraper_dir, headless=headless)
    site.login(username, password)
    results = site.search(search_terms=case_ids)
    assert len(results) == 1
    # Scrapes Case Detail page HTML by default
    assert 'page_source' in results[0].data.keys()


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
def test_skip_case_details(test_input, headless, live_configs, court_scraper_dir):
    "should support option to skip scraping of case details"
    auth = live_configs['ga_dekalb']
    username = auth['username']
    password = auth['password']
    url, case_ids = test_input
    site = OdysseySite(url, download_dir=court_scraper_dir, headless=headless)
    site.login(username, password)
    results = site.search(search_terms=case_ids, case_details=False)
    # Should *NOT* have case detail HTML stored on return object
    assert len(results) == 1
    assert 'page_source' not in results[0].data.keys()
