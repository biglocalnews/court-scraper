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

def test_parties(case_detail_html):
    "should extract parties"
    cdp = CaseDetailParser(case_detail_html)
    expected = [
        {
            'party_type': 'Plaintiff', 
            'party_name': 'Johnson, Arthur', 
            'address': '3000 Kelley Chapel RD Decatur GA 30034', 
            'attorney': 'Pro Se'
        }, 
        {
            'party_type': 'Defendant', 
            'party_name': 'LAKE, JARROD', 
            'address': '2755 KNOLLIGEN DR DECATUR GA 30034', 
            'attorney': 'Pro Se'
        }, 
        {
            'party_type': 'Defendant', 
            'party_name': 'MOORE, PAULA'
        }
    ]
    assert cdp.parties == expected

def test_disposition(case_detail_html): 
    "should extract disposition"
    cdp = CaseDetailParser(case_detail_html)
    expected = [
        {
            'judgment_date': '01/28/2019',
            'judgment': 'Dismissed with Prejudice'
        }
    ]
    assert cdp.disposition == expected

def test_multiple_dispositions(): 
    "should extract more than one disposition"
    html = read_fixture(
        'ga_dekalb/19D78499.html'
    )
    cdp = CaseDetailParser(html)
    expected = [
        {
            'judgment_date': '05/31/2019',
            'judgment': 'Writ Issued'
        },
        {
            'judgment_date': '06/03/2019',
            'judgment': 'Dismissed without Prejudice'
        }
    ]
    assert cdp.disposition == expected

def test_party_respondant(): 
    "should extract parties labelled as respondants"
    html = read_fixture(
        'ga_dekalb/21D06499.html'
    )
    cdp = CaseDetailParser(html)
    expected = [
        {
            'party_type': 'Respondant', 
            'party_name': '(Participant) BRANTLEY, CHEKASHA', 
            'address': '1431 COBB BRANCH DR DECATUR GA 30032'
        }, 
        {
            'party_type': 'Plaintiff', 
            'party_name': 'owner: VSPATL c/o SYLVAN HOMES LLC', 
            'address': '3495 PIEDMONT ROAD, BDLG 11, SUTIE 302 ATLANTA GA 30305', 
            'attorney': 'Lead Attorney Wilson, Lynn M.'
        }, 
        {
            'party_type': 'Defendant', 
            'party_name': 'OCCUPANTS, UNAUTHORIZED', 
            'address': '1431 COVV BRANCH DR DECATUR GA 30032'
        }
    ]
    assert cdp.parties == expected

def test_party_no_address(): 
    "should extract parties with missing address"
    html = read_fixture(
        'ga_dekalb/17D27499.html'
    )
    cdp = CaseDetailParser(html)
    expected = [
        {
            'party_type': 'Plaintiff', 
            'party_name': 'OAKS AT STONECREST', 
            'attorney': 'Lead Attorney Murphy, Andrew T'
        }, 
        {
            'party_type': 'Defendant', 
            'party_name': 'Hardison, Kenny', 
            'address': '2795 Evans Mill RD UNIT 2503 Lithonia GA 30058',
            'attorney': 'Pro Se'
        },
        {
            'party_type': 'Defendant', 
            'party_name': 'ALL OTHER', 
            'attorney': 'Pro Se'
        }
    ]
    assert cdp.parties == expected

def test_disposition_judgment_for(case_detail_html): 
    "should extract dispositions with judgment_for"
    html = read_fixture(
        'ga_dekalb/17D22499.html'
    )
    cdp = CaseDetailParser(html)
    expected = [
        {
            'judgment_date': '09/14/2017', 
            'judgment': 'Order and Judgment', 
            'judgment_for': 'Plaintiff'
        }
    ]
    assert cdp.disposition == expected
