from pathlib import Path
from unittest.mock import call, patch, MagicMock, Mock

import pytest

from .conftest import (
    config_path,
    court_scraper_dir,
    file_contents
)
from court_scraper.case_info import CaseInfo
from court_scraper.runner import Runner


@pytest.mark.usefixtures('create_scraper_dir', 'create_config')
def test_site_calls(court_scraper_dir, config_path):
    site_class = Mock(name='OdysseySite')
    to_patch = 'court_scraper.runner.Runner._get_site_class'
    with patch(to_patch) as mock_method:
        mock_method.return_value = site_class
        r = Runner(
            court_scraper_dir,
            config_path,
            'ga_dekalb'
        )
        r.search(search_terms=['foo'])
        username = 'user1@example.com'
        password = 'SECRETPASS'
        expected_args = (
            'https://ody.dekalbcountyga.gov/portal/Home/Dashboard/29',
            court_scraper_dir,
        )
        expected_kwargs = {'headless': True}
        # Get the args and kwargs (2nd and 3rd items) from the 
        # first call which is Site instantiation
        args, kwargs = site_class.mock_calls[0][1:]
        assert args == expected_args
        assert kwargs == expected_kwargs
        login_call, search_call = site_class.mock_calls[1:3]
        assert login_call == call().login(username, password)
        assert search_call == call().search(search_terms=['foo'])


@pytest.mark.usefixtures('create_scraper_dir', 'create_config')
def test_page_source_caching(court_scraper_dir, config_path):
    case = CaseInfo({
        'number': '20A123',
        'page_source': '<html>foo</html>'
    })
    r = Runner(
        court_scraper_dir,
        config_path,
        'ga_dekalb'
    )
    # Supply CaseInfo instances in a list
    r.cache_detail_pages([case])
    cache_file = Path(court_scraper_dir)\
        .joinpath('cache/ga_dekalb/20A123.html')
    actual = file_contents(cache_file)
    assert case.page_source == actual
