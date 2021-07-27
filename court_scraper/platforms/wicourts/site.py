from datetime import date

import requests

from court_scraper.base.selenium_site import SeleniumSite
from court_scraper.case_info import CaseInfo
from court_scraper.utils import dates_for_range
#from .pages.case_detail import CaseDetails
from .pages.search import SearchPage

from .search_api import SearchApi


class SearchConfigurationError(Exception): pass


class WicourtsSite(SeleniumSite):

    current_day = date.today().strftime("%Y-%m-%d")

    def __init__(self, place_id, captcha_api_key=None):
        self.captcha_api_key = captcha_api_key
        self.place_id = place_id
        self.url = "https://wcca.wicourts.gov/advanced.html"

    def search_by_date(self,
            start_date=None,
            end_date=None,
            case_details=False,
            case_types=[],
            download_dir=None,
            headless=True
        ):
        """
        Scrape case metadata and/or details by date ranges.

        Defaults to current day if no dates provided. Supports
        the ability to pass in additional query parameters supported
        by the Advanced Search in order to further limit search results.

        Args:

            start_date (str): start date in YYYY-MM-DD format (optional)
            end_date (str): end date in YYYY-MM-DD format (optional)
            case_details (boolean): Whether to scrape detailed case data. (optional; defaults to False)
            case_types (list<str>): One or more case type codes (optional)
            download_dir (str): Path for Selenium download directory (Only required for case detail scraping)
            headless (boolean): Run Selenium in headless mode for case detail searches (defaults to True)

        Returns:
            List of CaseInfo instances

        """
        if not start_date:
            start_date, end_date = self.current_day, self.current_day
        results = []
        county = self.place_id[3:] # Clip the state prefix from place_id
        if case_details:
            results = self.search(
                download_dir,
                start_date=start_date,
                end_date=end_date,
                case_types=case_types,
                headless=headless
            )
        else:
            # Case metadata can be gathered using just Requests
            date_format = "%m-%d-%Y"
            dates = dates_for_range(start_date, end_date, output_format=date_format)
            for date_str in dates:
                api = SearchApi(county)
                extra_params = {}
                if case_types:
                    extra_params['caseType'] = ','.join(case_types)
                cases = api.search_by_filing_date(
                    date_str,
                    date_str,
                    extra_params
                )
                results.extend(cases)
        return results

    def search(self,
           download_dir,
           case_numbers=[],
           start_date=None,
           end_date=None,
           case_types=[],
           headless=True
        ):
        """
        Scrape detailed case information by case numbers or date range.


        If case numbers provided, scraper will perform a case number search.
        If start and end dates provide, scraper will search by date range.
        Either case numbers or dates are required, otherwise an error is raised.

        Args:

            download_dir (str): Path for Selenium download directory
            case_numbers (list<str>): List of case numbers to search (optional)
            start_date (str): start date in YYYY-MM-DD format (optional)
            end_date (str): end date in YYYY-MM-DD format (optional)
            case_types (list<str>): One or more case type codes for date-based searches (optional)
            headless (boolean): Run Selenium in headless mode for case detail searches (defaults to True)

        Returns:
            List of CaseInfo instances

        """
        if not case_numbers and not start_date:
            raise SearchConfigurationError("You must provide case numbers or a date range!")
        self.download_dir = download_dir
        self.driver = self._init_chrome_driver(headless=headless)
        search_page = SearchPage(self.driver, self.captcha_api_key)
        results = []
        county = self.place_id[3:]
        try:
            if case_numbers:
                data = search_page.search_by_case_number(county, case_numbers)
            else:
                # Fall back to date-based search
                data = search_page.search_by_date(county, start_date, end_date, case_types=case_types)
            results.extend(data)
        finally:
            try:
                self.driver.quit()
            except AttributeError:
                pass
        return results
