from unittest.mock import call, patch, Mock

import pytest

from .conftest import (
    config_path,
    court_scraper_dir,
)
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
        expected_args = [
            'https://ody.dekalbcountyga.gov/portal/Home/Dashboard/29',
            username,
            password,
            court_scraper_dir
        ]
        site_class.assert_called_once_with(*expected_args)
        login_call, search_call = site_class.mock_calls[1:3]
        assert login_call == call().login(headless=True)
        assert search_call == call().search(search_terms=['foo'],headless=True)

