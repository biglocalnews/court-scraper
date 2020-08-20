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

