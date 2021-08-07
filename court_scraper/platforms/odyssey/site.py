from court_scraper.case_info import CaseInfo
from court_scraper.base.selenium_site import SeleniumSite

from .pages.case_detail import CaseDetailPage
from .pages.login import LoginPage
from .pages.portal import PortalPage
from .pages.search import SearchPage
from .pages.search_results import SearchResultsPage


class Site(SeleniumSite):

    def __init__(self, place_id, url=None, download_dir=None, headless=True):
        self.place_id = place_id
        self.site_url = url
        self.download_dir = download_dir or self.get_download_dir()
        self.driver = self._init_chrome_driver(headless=headless)

    def __repr__(self):
        return f'Odyssey ({self.place_id})'

    def login(self, username, password):
        self.username = username
        self.password = password
        login_page = LoginPage(
            self.driver,
            self.site_url,
            self.username,
            self.password
        )
        login_page.go_to()
        login_page.login()

    def go_to_home(self):
        self.driver.get(self.site_url)

    def search(self, case_numbers=[], case_details=False, timeout=60):
        """Search for cases by number.

        Supports search by precise case number or wild-card case number searches.

        Usage:

            # Precise number search
            site.search(case_numbers=['20CV000569','20CV000570'])

            # Wild-card search for 100 cases (in the 500s range)
            site.search(case_numbers=['20CV0005*'])

        Args:

            case_numbers (list<str>): List of case numbers
            case_details (boolean): Whether to scrape case details (default: True)
            timeout (int): Seconds before scraper times out (default: 60)

        Returns:

            List of CaseInfo classes

        """
        portal_page = PortalPage(self.driver)
        if portal_page.is_current_page:
            portal_page.go_to_smart_search()
        else:
            self.go_to_home()
        results = []
        CaseInfoKls = self._get_case_info_mapped_class()
        try:
            for case_number in case_numbers:
                search_page = SearchPage(self.driver)
                search_page.search_box = case_number
                search_page.submit_search(timeout)
                results_page = SearchResultsPage(self.driver)
                if results_page.results_found():
                    if results_page.has_paged_results_menu():
                        results_page.display_max_results()
                    for case_row in results_page.results:
                        row_data = case_row.metadata
                        if case_details:
                            case_row.detail_page_link.click()
                            detail_page = CaseDetailPage(self.driver)
                            row_data['page_source'] = detail_page.page_source
                            results_page.back_to_search_results()
                        ci = CaseInfoKls(row_data)
                        results.append(ci)
                results_page.back_to_smart_search_tab()
            return results
        finally:
            self.driver.quit()

    def _get_case_info_mapped_class(self):
        mapping = {
            'Case Number': 'number',
            'Style / Defendant': 'defendant',
            'File Date': 'filing_date',
            'Party Name': 'party',
            'Status': 'status',
            'Type': 'type',
            'Location': 'location',
        }
        CaseInfo._map = mapping
        return CaseInfo
