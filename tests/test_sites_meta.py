from unittest.mock import patch

import pytest

from .conftest import read_fixture, sites_csv_text
from court_scraper.sites_meta import SitesMeta


def test_url_lookup_by_state_county(sites_csv_text):
    to_patch = 'court_scraper.sites_meta.SitesMeta._get_sites_csv_text'
    with patch(to_patch) as mock_method:
        mock_method.return_value = sites_csv_text
        meta = SitesMeta()
        actual = meta.get_url(state='ga', county='dekalb')
        expected = 'https://ody.dekalbcountyga.gov/portal/Home/Dashboard/29'
        assert actual == expected


def test_url_lookup_multiname_county(sites_csv_text):
    to_patch = 'court_scraper.sites_meta.SitesMeta._get_sites_csv_text'
    with patch(to_patch) as mock_method:
        mock_method.return_value = sites_csv_text
        meta = SitesMeta()
        actual = meta.get_url(state='ca', county='san mateo')
        expected = 'https://odyportal-ext.sanmateocourt.org/Portal-External/Home/Dashboard/29'
        assert actual == expected


def test_get_by_place_id(sites_csv_text):
    to_patch = 'court_scraper.sites_meta.SitesMeta._get_sites_csv_text'
    with patch(to_patch) as mock_method:
        mock_method.return_value = sites_csv_text
        meta = SitesMeta()
        row = meta.get('ca_san_mateo')
        assert row['site_type'] == 'odyssey'
