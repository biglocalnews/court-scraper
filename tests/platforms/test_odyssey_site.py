from unittest.mock import call, patch

import pytest

from court_scraper.platforms.odyssey import Site as OdysseySite


@patch('court_scraper.platforms.odyssey.site.LoginPage')
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
            "ga_chatham",
            "https://cmsportal.chathamcounty.org/Portal/Home/Dashboard/29",
            ["MGCV20-00001"]
        ),
        (
            "ga_dekalb",
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
    place_id, url, case_ids = test_input
    site = OdysseySite(place_id, url=url, download_dir=court_scraper_dir, headless=headless)
    site.login(username, password)
    results = site.search(case_numbers=case_ids)
    assert len(results) == 1
    # Does *not* scrape Case Detail page (HTML) by default
    assert 'page_source' not in results[0].data.keys()


@pytest.mark.parametrize(
    "test_input",
    [
        (
            "ca_napa",
            "https://portal.napa.courts.ca.gov/Secure/Home/Dashboard/29",
            ["20CV000569"]
        ),
    ]
)
@pytest.mark.slow
@pytest.mark.webtest
def test_search_nologin_no_captcha(test_input, headless, court_scraper_dir):
    place_id, url, case_ids = test_input
    site = OdysseySite(place_id, url=url, download_dir=court_scraper_dir, headless=headless)
    results = site.search(case_numbers=case_ids)
    assert len(results) == 1


@pytest.mark.parametrize(
    "test_input",
    [
        (
            "ca_napa",
            "https://portal.napa.courts.ca.gov/Secure/Home/Dashboard/29",
            ["20CV000023"]
        ),
    ]
)
@pytest.mark.slow
@pytest.mark.webtest
def test_search_nologin_no_captcha_noresults(test_input, headless, court_scraper_dir):
    place_id, url, case_ids = test_input
    site = OdysseySite(place_id, url=url, download_dir=court_scraper_dir, headless=headless)
    results = site.search(case_numbers=case_ids)
    assert len(results) == 0


@pytest.mark.parametrize(
    "test_input",
    [
        (
            "ga_dekalb",
            "https://ody.dekalbcountyga.gov/portal/Home/Dashboard/29",
            ["19d89169"]
        ),
    ]
)
@pytest.mark.slow
@pytest.mark.webtest
def test_scrape_case_details(test_input, headless, live_configs, court_scraper_dir):
    "should support optional scraping of case details"
    auth = live_configs['ga_dekalb']
    username = auth['username']
    password = auth['password']
    place_id, url, case_ids = test_input
    site = OdysseySite(place_id, url=url, download_dir=court_scraper_dir, headless=headless)
    site.login(username, password)
    results = site.search(case_numbers=case_ids, case_details=True)
    # Should have case detail HTML stored on return object
    assert len(results) == 1
    assert 'page_source' in results[0].data.keys()


@pytest.mark.parametrize(
    "test_input",
    [
        (
            "ca_napa",
            "https://portal.napa.courts.ca.gov/Secure/Home/Dashboard/29",
            ["20CV0000*"]
        ),
    ]
)
@pytest.mark.slow
@pytest.mark.webtest
def test_maximize_displayed_results(test_input, headless, court_scraper_dir):
    "should automatically maximize the number of results displayed on results page"
    place_id, url, case_ids = test_input
    site = OdysseySite(place_id, url=url, download_dir=court_scraper_dir, headless=headless)
    results = site.search(case_numbers=case_ids)
    assert len(results) == 91


@pytest.mark.parametrize(
    "test_input",
    [
        (
            "ga_dekalb",
            "https://ody.dekalbcountyga.gov/portal/Home/Dashboard/29",
            ["19D93839"]
        ),
    ]
)
@pytest.mark.slow
@pytest.mark.webtest
def test_malformed_result_listing(test_input, headless, live_configs, court_scraper_dir):
    "should handle result listings that have an extra leading blank cell"
    auth = live_configs['ga_dekalb']
    username = auth['username']
    password = auth['password']
    place_id, url, case_ids = test_input
    site = OdysseySite(place_id, url=url, download_dir=court_scraper_dir, headless=headless)
    site.login(username, password)
    results = site.search(case_numbers=case_ids)
    assert len(results) == 1
    assert results[0].data['File Date'] == '10/02/2019'
