from court_scraper.case_info import CaseInfo


def test_attribute_mapping():
    mapping = { 'case_num': 'number', }
    data = { 'foo': 'bar', 'case_num': '1' }
    CaseInfo._map = mapping
    ci = CaseInfo(data)
    assert hasattr(ci, 'case_num') == False
    assert ci.number == '1'
    assert ci.foo == 'bar'


def test_standardized_data():
    mapping = {
        'case_num': 'number',
    }
    data = {
        'place_id': 'ga_dekalb',
        'case_num': '1',
        'status': 'Open',
        'foo': 'bar',
    }
    # Number should be standardized,
    # and foo should not appear
    expected = {
        'place_id': 'ga_dekalb',
        'number': '1',
        'status': 'Open',
    }
    CaseInfo._map = mapping
    ci = CaseInfo(data)
    assert ci.standard_data == expected
