import requests

from court_scraper.case_info import CaseInfo


class SearchApi:

    def __init__(self, county):
        self.url = "https://wcca.wicourts.gov/jsonPost/advancedCaseSearch"
        self.county = county


    def search_by_filing_date(self, start_date, end_date, extra_params={}):
        params = self._default_params
        params['filingDate'].update({
            'start': start_date,
            'end': end_date
        })
        params['countyNo'] = self._get_county_number(self.county)
        params.update(extra_params)
        search_response = requests.post(
            self.url,
            json=params
        )
        CaseInfoMapped = self._get_case_info_mapped_class()
        raw_cases = search_response.json()['result']['cases']
        return [CaseInfoMapped(data) for data in raw_cases]

    @property
    def _default_params(self):
        return {
            "attyType": "partyAtty",
            "countyNo": None,
            "filingDate":{
                "end": '', #MM-DD-YYYY
                "start": '', #MM-DD-YYYY
            },
            "includeMissingDob":True,
            "includeMissingMiddleName": True,
        }

    def _get_case_info_mapped_class(self):
        mapping = {
            'caseNo': 'number',
            'filingDate': 'filing_date',
            'partyName': 'party',
            'countyName': 'county',
            'countyNo': 'county_num',
        }
        CaseInfo._map = mapping
        return CaseInfo

    def _get_county_number(self, county):
        try:
            return self._county_num_lookup[county]['countyNo']
        except AttributeError:
            params = {"cachedData":{"counties":{}}}
            response = requests.post(
                'https://wcca.wicourts.gov/jsonPost',
                json=params
            )
            lookup = {
                cty['countyName'].lower().replace(' ', '_'):cty
                for cty in response.json()['cachedData']['counties']
            }
            self._county_num_lookup = lookup
            return lookup[county]['countyNo']
