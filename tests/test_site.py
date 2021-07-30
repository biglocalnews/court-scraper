from court_scraper import Site

import pytest


@pytest.mark.parametrize("place_id,site_class", [
    ("ga_dekalb", "Site"),
    ("ok_tulsa", "Site"),
    ("wi_milwaukee", "Site"),
])
def test_site(place_id, site_class):
    site = Site(place_id)
    assert site.__class__.__name__ == site_class
