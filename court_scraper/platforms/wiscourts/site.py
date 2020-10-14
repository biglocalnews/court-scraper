from court_scraper.case_info import CaseInfo
from court_scraper.base.selenium_site import SeleniumSite

from .pages.case_detail import CaseDetails
from .pages.search import SearchPage
from court_scraper.base._selenium_site_search_mixin import SiteSearchMixIn

class WiscourtSite(SeleniumSite, SiteSearchMixIn):

    def _get_case_info_mapped_class(self):
        mapping = {
            'case_num': 'number',
            'file_date': 'filing_date',
        }
        CaseInfo._map = mapping
        return CaseInfo