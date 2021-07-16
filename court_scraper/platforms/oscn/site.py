from datetime import date

TODAY=date.today().strftime("%m/%d/%y") # e.g 07/15/21

from court_scraper.case_info import CaseInfo
from .pages.case_detail import CaseDetailPage


class Site:

    def __init__(self, place_id):
        self.place_id = place_id

    def search(self, search_terms=[], **kwargs):
        """Search one or more case IDs in a given county.

        Args:
            search_terms (list<case numbers>): One or more case numbers

        Returns:

            List of CaseInfo classes

        """
        results = []
        # This will be a county typically, but we could at some
        # point support a state-wide search
        for case_number in search_terms:
            page = CaseDetailPage(self.place_id, case_number)
            # Prepare CaseInfo class instances
            # for any valid case detail pages
            data = { 'place_id': self.place_id }
            data.update(page.data)
            case = CaseInfo(data)
            results.append(case)
        return results

