from bs4 import BeautifulSoup

from court_scraper.case_info import CaseInfo


class SearchResultsPage:

    def __init__(self, place_id, html):
        self.place_id = place_id
        self.html = html

    @property
    def results(self):
        """Data from Search Results page

        Returns:

            List of CaseInfo instances
        """
        # Search results contain an entry for every party
        # to a case, so we need to deduplicate
        results = {}
        # Only grab result rows (i.e. skip header)
        for row in self.soup.table.find_all('tr', class_='resultTableRow'):
            case_id_cell, filing_date, case_name, found_party = row.find_all('td')
            case_id = case_id_cell.a.text.strip()
            try:
                case_info = results[case_id]
            except KeyError:
                data = {
                    'place_id': self.place_id,
                    'number': case_id,
                    'filing_date': filing_date.text.strip(),
                    'name': case_name.text.strip(),
                    'parties': []
                }
                case_info = CaseInfo(data)
                results[case_id] = case_info
            case_info.parties.append(found_party.text.strip())
        return list(results.values())

    @property
    def soup(self):
        try:
            return self._soup
        except AttributeError:
            self._soup = BeautifulSoup(self.html, 'html.parser')
            return self._soup
