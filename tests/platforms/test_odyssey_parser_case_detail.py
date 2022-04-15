import pytest

from court_scraper.platforms.odyssey.parsers.case_detail import (
    CaseDetailParser,
    MissingMetadataException,
)
from tests.conftest import read_fixture


@pytest.fixture(scope="session")
def case_detail_html():
    return read_fixture("ga_dekalb/19D67383.html")


def test_data_attribute(case_detail_html):
    "should have a data property that simplifies access to parsable data"
    cdp = CaseDetailParser(case_detail_html)
    data = cdp.data
    assert data["case_number"] == "19D67383"
    assert data["court"] == "Division 0"
    assert data["judicial_officer"] == "Anderson, Berryl A"
    assert data["file_date"] == "01/02/2019"
    assert data["case_type"] == "Magistrate Dispossessory - Non Payment of Rent"
    assert data["case_status"] == "Closed"
    assert data["disposition"] == [
        {"judgment_date": "01/28/2019", "judgment": "Dismissed with Prejudice"}
    ]
    assert data["parties"] == [
        {
            "party_type": "Plaintiff",
            "party_name": "Johnson, Arthur",
            "address": "3000 Kelley Chapel RD Decatur GA 30034",
            "attorney": "Pro Se",
        },
        {
            "party_type": "Defendant",
            "party_name": "LAKE, JARROD",
            "address": "2755 KNOLLIGEN DR DECATUR GA 30034",
            "attorney": "Pro Se",
        },
        {"party_type": "Defendant", "party_name": "MOORE, PAULA"},
    ]


def test_data_call_with_missing(case_detail_html):
    "should propagate an error on dynamic attributes missing from the page"
    html = read_fixture("ga_chatham/MGCV17-11099.html")
    cdp = CaseDetailParser(html)
    expected_err_msg = "HTML page has no Judicial Officer element"
    with pytest.raises(MissingMetadataException, match=expected_err_msg):
        assert cdp.data


def test_dynamic_attributes(case_detail_html):
    "should extract basic metadata dynamically"
    cdp = CaseDetailParser(case_detail_html)
    assert cdp.case_number == "19D67383"
    assert cdp.court == "Division 0"
    assert cdp.judicial_officer == "Anderson, Berryl A"
    assert cdp.file_date == "01/02/2019"
    assert cdp.case_type == "Magistrate Dispossessory - Non Payment of Rent"
    assert cdp.case_status == "Closed"


def test_parties(case_detail_html):
    "should extract parties"
    cdp = CaseDetailParser(case_detail_html)
    expected = [
        {
            "party_type": "Plaintiff",
            "party_name": "Johnson, Arthur",
            "address": "3000 Kelley Chapel RD Decatur GA 30034",
            "attorney": "Pro Se",
        },
        {
            "party_type": "Defendant",
            "party_name": "LAKE, JARROD",
            "address": "2755 KNOLLIGEN DR DECATUR GA 30034",
            "attorney": "Pro Se",
        },
        {"party_type": "Defendant", "party_name": "MOORE, PAULA"},
    ]
    assert cdp.parties == expected


def test_disposition(case_detail_html):
    "should extract disposition"
    cdp = CaseDetailParser(case_detail_html)
    expected = [{"judgment_date": "01/28/2019", "judgment": "Dismissed with Prejudice"}]
    assert cdp.disposition == expected


def test_multiple_dispositions():
    "should extract more than one disposition"
    html = read_fixture("ga_dekalb/19D78499.html")
    cdp = CaseDetailParser(html)
    expected = [
        {"judgment_date": "05/31/2019", "judgment": "Writ Issued"},
        {"judgment_date": "06/03/2019", "judgment": "Dismissed without Prejudice"},
    ]
    assert cdp.disposition == expected


def test_party_respondant():
    "should extract parties labelled as respondants"
    html = read_fixture("ga_dekalb/21D06499.html")
    cdp = CaseDetailParser(html)
    expected = [
        {
            "party_type": "Respondant",
            "party_name": "(Participant) BRANTLEY, CHEKASHA",
            "address": "1431 COBB BRANCH DR DECATUR GA 30032",
        },
        {
            "party_type": "Plaintiff",
            "party_name": "owner: VSPATL c/o SYLVAN HOMES LLC",
            "address": "3495 PIEDMONT ROAD, BDLG 11, SUTIE 302 ATLANTA GA 30305",
            "attorney": "Wilson, Lynn M.",
        },
        {
            "party_type": "Defendant",
            "party_name": "OCCUPANTS, UNAUTHORIZED",
            "address": "1431 COVV BRANCH DR DECATUR GA 30032",
        },
    ]
    assert cdp.parties == expected


def test_party_no_address():
    "should extract parties with missing address"
    html = read_fixture("ga_dekalb/17D27499.html")
    cdp = CaseDetailParser(html)
    expected = [
        {
            "party_type": "Plaintiff",
            "party_name": "OAKS AT STONECREST",
            "attorney": "Murphy, Andrew T",
        },
        {
            "party_type": "Defendant",
            "party_name": "Hardison, Kenny",
            "address": "2795 Evans Mill RD UNIT 2503 Lithonia GA 30058",
            "attorney": "Pro Se",
        },
        {"party_type": "Defendant", "party_name": "ALL OTHER", "attorney": "Pro Se"},
    ]
    assert cdp.parties == expected


def test_disposition_judgment_for(case_detail_html):
    "should extract dispositions with judgment_for"
    html = read_fixture("ga_dekalb/17D22499.html")
    cdp = CaseDetailParser(html)
    expected = [
        {
            "judgment_date": "09/14/2017",
            "judgment": "Order and Judgment",
            "judgment_for": "Plaintiff",
        }
    ]
    assert cdp.disposition == expected


def test_missing_dynamic_attribute(case_detail_html):
    "should propagate an error on dynamic attributes missing from the page"
    html = read_fixture("ga_chatham/MGCV17-11099.html")
    cdp = CaseDetailParser(html)
    expected_err_msg = "HTML page has no Judicial Officer element"
    with pytest.raises(MissingMetadataException, match=expected_err_msg):
        # All these dynamic attributes are typically present
        assert cdp.case_number == "MGCV17-11099"
        assert cdp.court == "Magistrate Civil"
        assert cdp.file_date == "08/14/2017"
        assert cdp.case_type == "General Civil Other"
        assert cdp.case_status == "Closed"
        # BUT...in Chatham and other places judicial officer is not present
        # This should raise a custom error
        assert cdp.judicial_officer is None


def test_extra_party_info(case_detail_html):
    "should extract only party name and attorney"
    # Some cases in Chatham have extra demographic info we ignore
    html = read_fixture("ga_chatham/MGCV20-10699.html")
    cdp = CaseDetailParser(html)
    expected = [
        {
            "party_type": "Plaintiff",
            "party_name": "A.J. Davis Property Management",
            "attorney": "Pro Se",
        },
        {
            "party_type": "Defendant",
            "party_name": "Chancey, John Patrick",
            "attorney": "Pro Se",
        },
        {
            "party_type": "Defendant",
            "party_name": "Hensley, Tabbatha Lynn",
            "attorney": "Pro Se",
        },
    ]
    assert cdp.parties == expected


def test_party_claimant(case_detail_html):
    "should extract parties"
    # Some Napa cases listed claimants and defendants
    # We are ignoring the claimants
    html = read_fixture("ca_napa/18CV001704.html")
    cdp = CaseDetailParser(html)
    expected = [
        {
            "party_type": "Plaintiff",
            "party_name": "Loving Life Real Estate, LLC",
            "attorney": "Myers, Alexander James",
        },
        {
            "party_type": "Defendant",
            "party_name": "Saldana, Jose",
            "address": "1413 Spring ST St Helena CA 94574",
            "attorney": "Pro Se",
        },
        {
            "party_type": "Defendant",
            "party_name": "Saldana, Amelia",
            "address": "1461 Main ST UNIT 631 St Helena CA 94574-7427",
            "attorney": "Pro Se",
        },
        {
            "party_type": "Defendant",
            "party_name": "Botto, Jorge",
            "address": "1413 Springs ST St Helena CA 94574",
            "attorney": "Pro Se Attorney Imperiale, James Thomas Work Phone 6196309615",
        },
    ]
    assert cdp.parties == expected


def test_multiple_attorneys(case_detail_html):
    "should extract parties and lead attorney"
    # Some cases in Snohomish have multipe attornies listed
    # We are only capturing the lead attorney
    html = read_fixture("wa_snohomish/17-2-01460-31.html")
    cdp = CaseDetailParser(html)
    expected = [
        {
            "party_type": "Plaintiff",
            "party_name": "Griffis Group Residential",
            "attorney": "NOVACK, LAUREN LESLIE",
        },
        {"party_type": "Defendant", "party_name": "Thompson, Brandon"},
    ]
    assert cdp.parties == expected
