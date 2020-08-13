from unittest.mock import patch

import pytest

from .conftest import read_fixture
from court_scraper.sites_meta import SitesMeta


@pytest.fixture
def sites_csv_text():
    return read_fixture('sites_meta.csv')


def test_url_lookup_by_state_county(sites_csv_text):
    to_patch = 'court_scraper.sites_meta.SitesMeta._get_sites_csv_text'
    with patch(to_patch) as mock_method:
        mock_method.return_value = sites_csv_text
        s = SitesMeta()
        actual = s.get_url(state='ga', county='dekalb')
        expected = 'https://ody.dekalbcountyga.gov/portal/Home/Dashboard/29'
        assert actual == expected
