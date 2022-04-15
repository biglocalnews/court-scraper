# Pages
# Logging
import logging

# Other stuff
from typing import List

from court_scraper.base.selenium_site import SeleniumSite
from court_scraper.case_info import CaseInfo
from court_scraper.utils import get_captcha_service_api_key

# Parsers
from . import parsers
from .pages.case_detail import CaseDetailPage
from .pages.home import HomePage
from .pages.search_results import SearchResultsPage
from .pages.search_selection import SearchSelectionPage
from .pages.search_trial_court import SearchTrialCourtPage

logger = logging.getLogger(__name__)


class Site(SeleniumSite):
    def __init__(self, place_id):
        self.captcha_api_key = get_captcha_service_api_key()
        self.place_id = place_id

    def __repr__(self):
        return "Iowa"

    def search(
        self, case_numbers=[], download_dir=None, headless=True
    ) -> List[CaseInfo]:
        """
        Conducts a search for each of the provided case numbers.

        The results are cached in the download directory.

        A list of CaseInfo objects are returned.
        """
        # Get everything configured
        logger.debug(f"Searching {len(case_numbers)} cases by case_number")
        self.download_dir = download_dir or self.get_download_dir()

        # Boot up the browser
        logger.debug(f"Initializing chromedriver (Headless={headless})")
        self.driver = self._init_chrome_driver(headless=headless)

        # Loop through the case numbers and grab em all
        case_list = []
        for num in case_numbers:
            logger.debug(f"Searching for {num} by case number")
            # Search it
            case = self._get_by_case_number(num)
            # Add it to the master list
            case_list.append(case)

        # Close the browser
        logger.debug("Closing browser")
        self.driver.quit()

        # Return the master list
        logger.debug(f"Returning {len(case_list)} CaseInfo objects")
        return case_list

    def search_by_date(
        self, start_date=None, end_date=None, case_details=False, case_types=[]
    ) -> List[CaseInfo]:
        raise NotImplementedError

    def login(self, username, password):
        # Perform login with username and password
        raise NotImplementedError

    def _get_by_case_number(self, case_number) -> CaseInfo:
        """
        Scrapes the data for the provided case number.

        Returns a CaseInfo object ready to be archived.
        """
        # Open the homepage
        home_page = HomePage(self.driver)
        home_page.open()

        # Open the search selection page
        home_page.start_search()
        search_selection_page = SearchSelectionPage(self.driver)

        # Open the trial court search page
        search_selection_page.open_trial_court_search()

        # Switch to the case number search tab
        search_trial_court_page = SearchTrialCourtPage(self.driver)
        search_trial_court_page.open_case_number_search_tab()

        # Parse the the id and type out of the case number
        case_dict = parsers.case_numbers.parse(case_number)

        # Convert our place_id into the county id that the form expects
        county_dict = parsers.counties.parse(self.place_id)

        # Search for the case
        search_trial_court_page.search_for_case_by_number(
            county_dict["id"], case_dict["type_id"], case_dict["id"]
        )

        # Open the case detail page
        search_results_page = SearchResultsPage(self.driver)
        search_results_page.open_case_detail_page(case_number)

        # Parse the case detail page
        case_detail_page = CaseDetailPage(self.driver)
        case_detail_page.open()

        # Parse the case detail page
        obj = CaseInfo(
            {
                "place_id": self.place_id,
                "number": case_number,
                "page_source": self.driver.page_source,
                "url": case_detail_page.url,
            }
        )

        # Return the result
        return obj
