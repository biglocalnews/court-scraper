from bs4 import BeautifulSoup

from court_scraper.case_info import CaseInfo


class DailyFilingsResultsPage:

    def __init__(self, place_id, html):
        self.place_id = place_id
        self.html = html

    @property
    def results(self):
        """Data from Daily Filings search results page

        Returns:

            List of CaseInfo instances

        """
        results = []
        tables = self.soup.find_all('table')
        for table in tables:
            results.extend(self._extract_case_data(table))
        return results

    def _extract_case_data(self, table):
        # Get section header
        data = []
        # Section headers precede table tag and
        # contain generic case types, e.g. 'Civil Misc. (CV)'
        case_type = table.find_previous('font').text.strip()
        for row in table.find_all('tr'):
            # Get case data
            cell1, cell2 = row.find_all('td')
            row_data = {
                'place_id': self.place_id,
                'type_short': case_type,
                'number': cell1.a.text.strip(),
                'parties_short': cell2.text.strip(),
            }
            case_info = CaseInfo(row_data)
            data.append(case_info)
        return data

    @property
    def soup(self):
        try:
            return self._soup
        except AttributeError:
            self._soup = BeautifulSoup(self.html, 'html.parser')
            return self._soup
