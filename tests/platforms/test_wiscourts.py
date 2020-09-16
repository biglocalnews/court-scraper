from unittest.mock import call, patch

import pytest

from court_scraper.platforms.wiscourts import WiscourtSite

@pytest.fixture
def mock_county():
    return 'milwaukee'

def mock_year():
    return '2020'

def mock_case_prefix():
    return 'sc'

@patch('court_scraper.platforms.oscn.site.search')
@patch('court_scraper.base.selenium_site.webdriver')
def test_search(webdriver_mock, search_page_mock):
    site = OSCNSite(
        'http://somesite.com',
        'user',
        'pass',
        '/some_path/'
    )
    test_result = site.search.most_recent_Case(mock_county, mock_year, mock_case_prefix)
    assert search.most_recent_case().called
    assert test_result