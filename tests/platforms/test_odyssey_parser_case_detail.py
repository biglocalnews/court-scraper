import pytest

from court_scraper.platforms.odyssey.parsers.case_detail import CaseDetailParser
from tests.conftest import read_fixture


@pytest.fixture(scope='session')
def case_detail_html():
    return read_fixture(
        'ga_dekalb/19D67383.html'
    )

def test_dynamic_attributes(case_detail_html):
    "should extract basic metadata dynamically"
    cdp = CaseDetailParser(case_detail_html)
    assert cdp.case_number == '19D67383'
    assert cdp.court == 'Division 0'
    assert cdp.judicial_officer == 'Anderson, Berryl A'
    assert cdp.file_date == '01/02/2019'
    assert cdp.case_type == 'Magistrate Dispossessory - Non Payment of Rent'
    assert cdp.case_status == 'Closed'


def test_plaintiffs(case_detail_html):
    "should extract plaintiffs"
    cdp = CaseDetailParser(case_detail_html)
    expected = [
        {
            'name': 'Johnson, Arthur',
            'address': '3000 Kelley Chapel RD; Decatur GA 30034',
            #'attorneys': ['Pro Se'],
        }
    ]
    assert cdp.plaintiffs == expected
