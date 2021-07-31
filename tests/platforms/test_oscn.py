from unittest import mock

import pytest

from court_scraper.platforms.oscn import Site as Oscn


@pytest.mark.vcr()
@pytest.mark.parametrize(
    "place_id,case_number,expected",
    [
        # Basic open case
        ('ok_tulsa', 'CJ-2021-2045', {
            'filing_date': '07/15/2021',
            'close_date': None,
            'judge': 'Civil Docket A',
            'type': 'Civil relief more than $10,000: FORECLOSURE'
        }),
        # Closed case
        ('ok_tulsa', 'CJ-2018-2919', {
            'filing_date': '07/12/2018',
            'close_date': '01/23/2019',
            'judge': 'Civil Docket B',
            'type': 'Civil relief more than $10,000: PREMISES LIABILITY'
        }),
        # Multi-word countycase
        ('ok_roger_mills', 'CV-2021-14', {
            'filing_date': '07/09/2021',
            'close_date': None,
            'judge': 'Weedon, Jill Carpenter',
            'type': 'Civil Misc.: AD VALOREM TAX APPEAL'
        })
    ]
)
def test_search_by_case_id(place_id, case_number, expected):
    site = Oscn(place_id)
    results = site.search(case_numbers=[case_number])
    assert site.place_id == place_id
    assert len(results) == 1
    case = results[0]
    assert case.place_id == place_id
    assert case.number == case_number
    assert case.html.startswith('<!DOCTYPE')
    assert case.filing_date == expected['filing_date']
    assert case.close_date == expected['close_date']
    assert case.type == expected['type']
    assert case.judge == expected['judge']

@pytest.mark.vcr()
def test_search_by_case_id_multiple_results():
    site = Oscn('ok_tulsa')
    case_numbers = ['CJ-2021-2045', 'CJ-2018-2919']
    results = site.search(case_numbers=case_numbers)
    assert len(results) == 2

@pytest.mark.vcr()
def test_date_search_basic():
    place_id = 'ok_roger_mills'
    day = '2021-07-09'
    case_number = 'CV-2021-14'
    site = Oscn(place_id)
    # Returns a SearchResults dict-like object
    results = site.search_by_date(start_date=day, end_date=day, case_details=False)
    # There should be a single entry for the searched date
    assert results.count_of_days == 1
    data = results[day]
    # There should only be a single case on this day
    assert len(data['cases']) == 1
    # Raw html should be stored in the date's dict value (e.g. for caching)
    assert 'html' in data
    case = data['cases'][0]
    # Check for presence of other expected data points
    assert case.place_id == place_id
    assert case.number == case_number
    assert case.type_short == 'Civil Misc. (CV)'
    assert case.parties_short == 'DCP OPERATING COMPANY LP v. ROGER MILLS COUNTY ASSESSOR'
    # And the absence of case detail, since we didn't
    # request case_detail page to be scraped
    assert getattr(case, 'judge', None) is None

@pytest.mark.vcr()
def test_date_search_no_results():
    place_id = 'ok_roger_mills'
    day = '2021-07-15'
    site = Oscn(place_id)
    # Returns a SearchResults dict-like object
    results = site.search_by_date(start_date=day, end_date=day, case_details=False)
    # There should be no results for this date
    assert results.count_of_days == 0


@pytest.mark.vcr()
def test_date_search_defaults_to_current_day():
    from court_scraper.platforms.oscn.site import Site as Oscn
    with mock.patch.object(Oscn, 'current_day', '2021-07-09'):
        place_id = 'ok_roger_mills'
        case_number = 'CV-2021-14'
        site = Oscn(place_id)
        # Returns a SearchResults dict-like object
        results = site.search_by_date(case_details=False)
        # There should be a single entry for the searched date
        assert results.count_of_days == 1
        # Raw html should be stored in the date's dict value (e.g. for caching)
        data = results['2021-07-09']
        assert 'html' in data
        case = data['cases'][0]
        # Check for presence of other expected data points
        assert case.place_id == place_id

@pytest.mark.vcr()
def test_date_search_many_results():
    place_id = 'ok_tulsa'
    day = '2021-07-15'
    site = Oscn(place_id)
    # Returns a SearchResults dict-like object
    results = site.search_by_date(start_date=day, end_date=day, case_details=False)
    # There should be a single entry for the searched date
    assert results.count_of_days == 1
    # There should be many cases on this day
    assert len(results.cases) == 219
    # Test case type section headers
    expected_case_types = [
        'Civil Misc. (CV)',
        'Civil relief less than $10,000 (CS)',
        'Civil relief more than $10,000 (CJ)',
        'Criminal Felony (CF)',
        'Criminal Miscellaneous (MI)',
        'Criminal Misdemeanor (CM)',
        'Family and Domestic (FD)',
        'Marriage license (ML)',
        "Minister's Credentials (MC)",
        'Miscellaneous Receipts - Criminal (MRC)',
        'Paternity (FP)',
        'Probate (PB)',
        'Protective Order (PO)',
        'Small Claims (SC)'
    ]
    # Quite a few case types as well
    assert results.case_types == expected_case_types

@pytest.mark.vcr()
def test_date_search_multiple_day_results():
    place_id = 'ok_roger_mills'
    start = '2021-07-08'
    end = '2021-07-09'
    site = Oscn(place_id)
    # Returns a SearchResults dict-like object
    results = site.search_by_date(start_date=start, end_date=end, case_details=False)
    # There should be a single entry for the searched date
    assert results.count_of_days == 2
    # There should be many cases on this day
    assert len(results.cases) == 2
    assert results.dates == [start, end]
    first = results[start]['cases'][0]
    second = results[end]['cases'][0]
    assert first.number == 'CV-2021-13'
    assert second.number == 'CV-2021-14'


@pytest.mark.vcr()
def test_date_search_with_case_details():
    place_id = 'ok_roger_mills'
    day = '2021-07-09'
    case_number = 'CV-2021-14'
    site = Oscn(place_id)
    # Returns a SearchResults dict-like object
    # Here we set case_details to True to trigger detail page scraping
    results = site.search_by_date(start_date=day, end_date=day, case_details=True)
    # There should be a single entry for the searched date
    assert results.count_of_days == 1
    data = results[day]
    # There should only be a single case on this day
    assert len(data['cases']) == 1
    # Raw html should be stored in the date's dict value (e.g. for caching)
    assert 'html' in data
    case = data['cases'][0]
    # Check for presence of other expected data points
    assert case.place_id == place_id
    assert case.number == case_number
    assert case.type_short == 'Civil Misc. (CV)'
    assert case.parties_short == 'DCP OPERATING COMPANY LP v. ROGER MILLS COUNTY ASSESSOR'
    # Case details should be available
    assert case.judge == 'Weedon, Jill Carpenter'
    assert case.close_date == None


@pytest.mark.vcr()
def test_date_search_multiple_cases():
    place_id = 'ok_roger_mills'
    day = '2021-07-12'
    site = Oscn(place_id)
    # Set case_details to True to trigger detail page scraping
    results = site.search_by_date(start_date=day, end_date=day, case_details=True)
    # There should be a single entry for the searched date
    assert results.count_of_days == 1
    data = results[day]
    # There should two cases on this day
    assert len(data['cases']) == 2
    first, second = results.cases
    # Check for presence of other expected data points
    assert first.number == 'TR-2021-161'
    assert second.number == 'TR-2021-162'
    # Case details should be available
    # Judge
    assert first.judge == 'VerSteeg, F. Pat'
    assert second.judge == 'VerSteeg, F. Pat'
    # Closed date
    assert first.close_date == None
    assert second.close_date == '07/15/2021'
