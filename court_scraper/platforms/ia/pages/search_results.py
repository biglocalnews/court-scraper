# Scraping tools
# Logging
import logging

from selenium.webdriver.common.by import By

from court_scraper.base.selenium_helpers import SeleniumHelpers

logger = logging.getLogger(__name__)


class SearchResultsPageLocators:
    """
    Identifiers for important elements on the search results page.
    """

    LINK_LIST = (By.XPATH, "//a")


class SearchResultsPage(SeleniumHelpers):
    """
    Interface for interacting with the search results page.
    """

    locators = SearchResultsPageLocators
    url = "https://www.iowacourts.state.ia.us/ESAWebApp/TrialCaseSearchResultServlet"

    def __init__(self, driver):
        self.driver = driver
        self.timeout = 5

    def _get_link_by_case_number(self, case_number):
        """
        Sifts through the links on the page to find one for the provided case number.
        """
        # Get all the links
        link_list = self._get_elements_by_locator(self.locators.LINK_LIST)

        # Count em
        link_count = len(link_list)
        logger.debug(f"Links found: {link_count}")

        # If there's zero, throw up your hands
        if link_list == 0:
            raise ValueError
        # If there's 1, return it
        elif link_list == 1:
            return link_list[0]

        # If there's more than one, we'll start by deduplicating them
        text_list = [a.text for a in link_list]
        unique_text_list = set(text_list)

        # If there's only one, we can pass back the first link safely
        if len(unique_text_list) == 1:
            return link_list[0]

        # If there's more than one, we are in trouble.
        logger.error("More than one link found in search results")
        raise ValueError

    def open_case_detail_page(self, case_number):
        logger.debug(f"Opening case detail page for {case_number}")
        link = self._get_link_by_case_number(case_number)
        link.click()
