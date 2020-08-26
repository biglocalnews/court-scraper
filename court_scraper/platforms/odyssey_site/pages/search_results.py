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
class SearchResults:

    locator = SearchResultsPageLocators.RESULT_ROWS

    def __get__(self, obj, owner):
        """Gets the text of the specified object"""
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_elements(*self.locator)
        )
        elements = driver.find_elements(*self.locator)
        case_rows = self._prep_case_rows(elements)
        return case_rows

    def _prep_case_rows(self, elements):
        case_rows = []
        for el in elements:
            row = ResultRow(el)
            if row.is_case_row:
                case_rows.append(row)
        return case_rows


class ResultRow:

    def __init__(self, row_element):
        self.el = row_element

    @property
    def metadata(self):
        case_detail_url = self.el.find_element(
                *SearchResultsPageLocators.CASE_DETAIL_LINK
            ).get_attribute('data-url')
        case_num, style_def, file_date, status, party_name = [
            field.strip() for field in self.inner_text.split('\t')
        ]
        return {
            'case_num': case_num,
            'style_defendant': style_def,
            'file_date': file_date,
            'status': status,
            'party_name': party_name,
            'case_detail_url': case_detail_url,
        }

    @property
    def is_case_row(self):
        case_num = self.inner_text.split('\t')[0]
        case_num_pattern = r'^\d\d[A-Z0-9]+$'
        if re.match(case_num_pattern, case_num):
            return True
        return False

    @property
    def inner_text(self):
        return self.el.get_attribute('innerText').strip('\t')

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
