import pytest

from court_scraper.platforms.oscn import Oscn


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
        })
    ]
)
def test_search_by_case_id(place_id, case_number, expected):
    site = Oscn(place_id)
    results = site.search(search_terms=[case_number])
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


