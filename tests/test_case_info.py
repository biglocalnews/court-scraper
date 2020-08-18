from court_scraper.case_info import CaseInfo


def test_case_info():
    mapping = { 'case_num': 'number', }
    data = { 'foo': 'bar', 'case_num': '1' }
    CaseInfo._map = mapping
    ci = CaseInfo(data)
    assert hasattr(ci, 'case_num') == False
    assert ci.number == '1'
    assert ci.foo == 'bar'
