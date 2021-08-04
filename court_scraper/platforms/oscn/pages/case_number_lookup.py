from court_scraper.case_info import CaseInfo
from .case_detail import CaseDetailPage


class CaseNumberLookup:

    def __init__(self, place_id):
        self.place_id = place_id

    def search(self, case_numbers=[]):
        results = []
        for case_number in case_numbers:
            page = CaseDetailPage(self.place_id, case_number)
            # Prepare CaseInfo class instances
            # for any valid case detail pages
            data = {'place_id': self.place_id}
            data.update(page.data)
            case = CaseInfo(data)
            results.append(case)
        return results
