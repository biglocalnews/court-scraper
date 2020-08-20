from court_scraper.case_info import CaseInfo
from court_scraper.base.selenium_site import SeleniumSite

from .pages.case_detail import CaseDetailPage
from .pages.login import LoginPage
from .pages.portal import PortalPage
from .pages.search import SearchPage
from .pages.search_results import SearchResultsPage


class OdysseySite(SeleniumSite):

    def __init__(self, url, username, password, download_dir, timeout=60):
        self.site_url = url
        self.username = username
        self.password = password
        self.download_dir = download_dir
        self.timeout = timeout

    def login(self, headless=True):
        self.driver = self._init_chrome_driver(headless=headless)
        login_page = LoginPage(
            self.driver,
            self.site_url,
            self.username,
            self.password
        )
        login_page.go_to()
        login_page.login()

    def search(self, search_terms=[], headless=True):
        portal_page = PortalPage(self.driver)
        portal_page.go_to_smart_search()
        results = []
        CaseInfoKls = self._get_case_info_mapped_class()
        try:
            for term in search_terms:
                search_page = SearchPage(self.driver)
                search_page.search_box = term
                search_page.submit_search(self.timeout)
                results_page = SearchResultsPage(self.driver)
                if results_page.results_found():
                    for case_row in results_page.results:
                        row_data = case_row.metadata
                        case_row.detail_page_link.click()
                        detail_page = CaseDetailPage(self.driver)
                        row_data['page_source'] = detail_page.page_source
                        ci = CaseInfoKls(row_data)
                        results.append(ci)
                        results_page.back_to_search_results()
                results_page.back_to_smart_search_tab()
            return results
        finally:
            self.driver.quit()

    def _get_case_info_mapped_class(self):
        mapping = {
            'case_num': 'number',
            'file_date': 'filing_date',
        }
        CaseInfo._map = mapping
        return CaseInfo

    

