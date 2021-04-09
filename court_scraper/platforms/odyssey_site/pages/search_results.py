import re

from retrying import retry
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from .base import BasePage


# Locators
class SearchResultsPageLocators:

    RESULTS_DIV = (By.CSS_SELECTOR, '#SmartSearchResults')
    NO_RESULTS_MSG = (By.XPATH, '//*[@id="ui-tabs-1"]/div/p')
    CASE_DETAIL_LINK = (By.CSS_SELECTOR, 'a.caseLink')
    RESULT_HEADERS = (By.CSS_SELECTOR, 'th.k-header')
    # Get table rows that are the grandparent of case links;
    # they contain all case metadata in search results.
    RESULT_ROWS = (By.XPATH, "//a[@class='caseLink']/../..")
    # After a successful search, the page listing all cases
    # can be accessed as the second "step" in a 3-part series
    # of tabs. When a case link is clicked, that changes
    # screen to the 3rd step. To return to the case results list,
    # you must use the below selector and click the link
    CASE_RESULTS_TAB = (
        By.XPATH,
        "//p[@class='step-label' and contains(text(), 'Search Results')]/.."
    )
    SMART_SEARCH_TAB = (
         By.XPATH,
        "//p[@class='step-label' and contains(text(), 'Smart Search')]/.."
    )


# Elements
class ResultHeaders:
    """Gets field names in search results"""

    locator = SearchResultsPageLocators.RESULT_HEADERS

    def __init__(self, driver):
        self.driver = driver

    @property
    def values(self):
        driver = self.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_elements(*self.locator)
        )
        return [
            el.text.strip()
            for el in driver.find_elements(*self.locator)
            if el.text.strip()
        ]


class SearchResults:

    locator = SearchResultsPageLocators.RESULT_ROWS

    def __get__(self, obj, owner):
        """Gets the text of the specified object"""
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_elements(*self.locator)
        )
        elements = driver.find_elements(*self.locator)
        headers = ResultHeaders(driver).values
        case_rows = self._prep_case_rows(headers, elements)
        return case_rows

    def _prep_case_rows(self, headers, elements):
        case_rows = []
        for el in elements:
            case_rows.append(ResultRow(headers, el))
        return case_rows


class ResultRow:

    def __init__(self, headers, row_element):
        self.headers = headers
        self.el = row_element

    @property
    def metadata(self):
        case_detail_url = self.el.find_element(
                *SearchResultsPageLocators.CASE_DETAIL_LINK
            ).get_attribute('data-url')
        data = dict(zip(self.headers, self.values))
        data['case_detail_url'] = case_detail_url
        return data

    @property
    def values(self):
        return [
            el.text.strip() for el in self.el.find_elements_by_xpath('child::*')
            if el.text.strip()
        ]

    @property
    def detail_page_link(self):
        return self.el.find_element(
            *SearchResultsPageLocators.CASE_DETAIL_LINK
        )


class SearchResultsPage(BasePage):

    results = SearchResults()

    @retry(
        stop_max_attempt_number=7,
        stop_max_delay=30000,
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000
    )
    def results_found(self):
        found = False
        try:
            results_el = self.driver.find_element(
                *SearchResultsPageLocators.RESULTS_DIV
            )
            found = True
        except NoSuchElementException:
            results_el = None
        try:
            no_results_el = self.driver.find_element(
                *SearchResultsPageLocators.NO_RESULTS_MSG
            )
        except NoSuchElementException:
            no_results_el = ''
        if results_el and found == True:
            return True
        elif 'No cases match' in no_results_el.get_attribute('innerText'):
            return False
        else:
            raise Exception("Search not yet completed")

    def back_to_search_results(self):
        self._locate_and_click(
            SearchResultsPageLocators.CASE_RESULTS_TAB
        )

    def back_to_smart_search_tab(self):
        self._locate_and_click(
            SearchResultsPageLocators.SMART_SEARCH_TAB
        )

    def _locate_and_click(self, locator):
        self.driver.find_element(*locator).click()
