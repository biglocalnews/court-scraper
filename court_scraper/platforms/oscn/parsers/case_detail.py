import re
from bs4 import BeautifulSoup


class CaseDetailParser:

    def __init__(self, html):
        self.html = html

    def parse(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        payload = {
            'filing_date': self._filing_date(soup),
            'close_date': self._close_date(soup),
            'judge': self._judge(soup),
            'type': self._type(soup),
        }
        return payload

    def _filing_date(self, soup):
        second_cell = self._get_top_row_second_cell(soup)
        # Text is collapsed due to <br> tags. For example:
        #   Filed: 07/15/2021Judge: Civil Docket A'
        return self._regextract(r'Filed: (\d{1,2}/\d{1,2}/\d{4})', second_cell.text)

    def _close_date(self, soup):
        second_cell = self._get_top_row_second_cell(soup)
        return self._regextract(r'Closed: (\d{1,2}/\d{1,2}/\d{4})', second_cell.text)

    def _judge(self, soup):
        second_cell = self._get_top_row_second_cell(soup)
        # Text is collapsed due to <br> tags. For example:
        #   Filed: 07/15/2021Judge: Civil Docket A'
        return self._regextract(r'Judge: (.+)', second_cell.text.strip())

    def _type(self, soup):
        # Civil relief more than $10,000: FORECLOSURE
        second_cell = self._get_top_row_second_cell(soup)
        return second_cell.find('strong').text.strip().split('(')[-1].rstrip(')')

    def _get_top_row_second_cell(self, soup):
        try:
            return self._top_row_second_cell
        except AttributeError:
            h2 = soup.find('h2', class_='styletop')
            table = h2.find_next('table')
            first_row = table.find_all('tr')[0]
            self._top_row_second_cell = first_row.find_all('td')[-1]
        return self._top_row_second_cell

    def _regextract(self, pattern, text):
        try:
            return re.search(pattern, text).groups()[0]
        except AttributeError:
            return None
