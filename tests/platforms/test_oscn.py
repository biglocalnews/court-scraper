from unittest.mock import call, patch

import pytest

from court_scraper.platforms.oscn.pages.search import *

@pytest.fixture
def mock_county():
    return 'tulsa'

@pytest.fixture
def mock_year():
    return '2020'

@pytest.fixture
def mock_case_prefix():
    return 'sc'

@patch('court_scraper.platforms.oscn.search')
def test_search(mock_county, mock_year, mock_case_prefix):
    test_result = search.most_recent_case(mock_county, mock_year, mock_case_prefix)
    assert search.most_recent_case().called
    assert test_result