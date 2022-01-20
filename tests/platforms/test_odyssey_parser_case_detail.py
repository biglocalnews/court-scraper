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
            'attorney': 'Wilson, Lynn M.'
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
            'attorney': 'Murphy, Andrew T'
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

def test_dynamic_attributes_chatham(case_detail_html):
    "should extract basic metadata dynamically"
    html = read_fixture(
        'ga_chatham/MGCV17-11099.html'
    )
    cdp = CaseDetailParser(html)
    assert cdp.case_number == 'MGCV17-11099'
    assert cdp.court == 'Magistrate Civil'
    #assert cdp.judicial_officer == ''
    assert cdp.file_date == '08/14/2017'
    assert cdp.case_type == 'General Civil Other'
    assert cdp.case_status == 'Closed'

def test_parties_chatham(case_detail_html):
    "should extract parties"
    html = read_fixture(
        'ga_chatham/MGCV17-11099.html'
    )
    cdp = CaseDetailParser(html)    
    expected = [
        {
            'party_type': 'Plaintiff', 
            'party_name': 'TD Bank USA, N.A.', 
            'attorney': 'Woolaston, Dorian'
        }, 
        {
            'party_type': 'Defendant', 
            'party_name': 'Monteith, Henry C.', 
            'attorney': 'Pro Se'
        }
    ]
    assert cdp.parties == expected

def test_multiple_parties_chatham(case_detail_html):
    "should extract multiple parties"
    html = read_fixture(
        'ga_chatham/MGCV20-10699.html'
    )
    cdp = CaseDetailParser(html)    
    expected = [
        {
            'party_type': 'Plaintiff', 
            'party_name': 'A.J. Davis Property Management', 
            'attorney': 'Pro Se'
        }, 
        {
            'party_type': 'Defendant', 
            'party_name': 'Chancey, John Patrick', 
            'attorney': 'Pro Se'
        }, 
        {
            'party_type': 'Defendant', 
            'party_name': 'Hensley, Tabbatha Lynn', 
            'attorney': 'Pro Se'
        }
    ]
    assert cdp.parties == expected

def test_disposition_chatham(case_detail_html): 
    "should extract disposition"
    html = read_fixture(
        'ga_chatham/MGCV20-10699.html'
    )
    cdp = CaseDetailParser(html)    
    expected = [
        {
            'judgment_date': '01/07/2021',
            'judgment': 'Judgment',
            'judgment_for': 'Plaintiff'
        }
    ]
    assert cdp.disposition == expected

def test_dynamic_attributes_napa(case_detail_html):
    "should extract basic metadata dynamically"
    html = read_fixture(
        'ca_napa/19CV000014.html'
    )
    cdp = CaseDetailParser(html)
    assert cdp.case_number == '19CV000014'
    assert cdp.court == 'Superior Court of Napa - Civil'
    #assert cdp.judicial_officer == ''
    assert cdp.file_date == '01/03/2019'
    assert cdp.case_type == 'Unlawful Detainer Residential Limited (32) - under 10,000'
    assert cdp.case_status == 'Inactive'

def test_parties_napa(case_detail_html):
    "should extract parties"
    html = read_fixture(
        'ca_napa/19CV000014.html'
    )
    cdp = CaseDetailParser(html)    
    expected = [
        {
            'party_type': 'Plaintiff', 
            'party_name': 'Cryrag, Inc.', 
            'attorney': 'Myers, Alexander James'
        }, 
        {
            'party_type': 'Defendant', 
            'party_name': 'Lemus, Ricardo',
            'address': '39 Coombs ST Napa CA 94559', 
            'attorney': 'Pro Se'
        },
        {
            'party_type': 'Defendant', 
            'party_name': 'Patsias, Athanasia',
            'address': '39 Coombs ST Napa CA 94559', 
            'attorney': 'Pro Se'
        }
    ]
    assert cdp.parties == expected

def test_disposition_napa(case_detail_html): 
    "should extract disposition"
    html = read_fixture(
        'ca_napa/19CV000014.html'
    )
    cdp = CaseDetailParser(html)    
    expected = [
        {
            'judgment_date': '02/08/2019',
            'judgment': 'Judgment - Court Finding'
        }
    ]
    assert cdp.disposition == expected

def test_dynamic_attributes_snohomish(case_detail_html):
    "should extract basic metadata dynamically"
    html = read_fixture(
        'wa_snohomish/17-2-01460-31.html'
    )
    cdp = CaseDetailParser(html)
    assert cdp.case_number == '17-2-01460-31'
    assert cdp.court == 'Snohomish'
    #assert cdp.judicial_officer == ''
    assert cdp.file_date == '02/17/2017'
    assert cdp.case_type == 'UND Residential Unlawful Detainer'
    assert cdp.case_status == 'Completed/Re-Completed'

def test_parties_snohomish(case_detail_html):
    "should extract parties"
    html = read_fixture(
        'wa_snohomish/17-2-01460-31.html'
    )
    cdp = CaseDetailParser(html)    
    expected = [
        {
            'party_type': 'Plaintiff', 
            'party_name': 'Griffis Group Residential', 
            'attorney': 'NOVACK, LAUREN LESLIE'
        }, 
        {
            'party_type': 'Defendant', 
            'party_name': 'Thompson, Brandon'
        }
    ]
    assert cdp.parties == expected
