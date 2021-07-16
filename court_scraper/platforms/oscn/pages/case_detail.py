import requests

from ..parsers.case_detail import CaseDetailParser


class CaseDetailPage:

    def __init__(self, place_id, case_number, parser_kls=CaseDetailParser):
        self.url = 'https://www.oscn.net/dockets/GetCaseInformation.aspx'
        self.place_id = place_id
        self.case_number = case_number
        self.parser_kls = parser_kls

    @property
    def data(self):
        payload = {
            'number': self.case_number,
            'html': self.html,
        }
        parser = self.parser_kls(self.html)
        extra_data = parser.parse()
        payload.update(extra_data)
        return payload

    @property
    def html(self):
        try:
            return self._output
        except AttributeError:
            payload = {
                'db': self._place,
                'number': self.case_number,
            }
            response = requests.get(self.url, params=payload)
            _html = response.text
            self._output = _html
            return _html

    @property
    def _place(self):
        county_bits = self.place_id.split('_')[1:]
        return "".join(county_bits).lower().strip()
