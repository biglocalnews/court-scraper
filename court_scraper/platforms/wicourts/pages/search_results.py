from urllib.parse import parse_qs

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from court_scraper.base.selenium_helpers import SeleniumHelpers
from ..search_api import SearchApi


class ResultsLocators:

    SHOW_ALL_RESULTS = (By.XPATH, '//*[@id="caseSearchResults_length"]/label/select/option[5]')
    RESULTS_TABLE_ROWS = (By.XPATH, '//*[@id="caseSearchResults"]/tbody/tr')
    RESULTS_TABLE = (By.XPATH, '//*[@id="caseSearchResults"]')
    YEAR_FILTER = (By.XPATH, '//*[@id="caseSearchResults"]/thead/tr[2]/td[1]/input')
    SINGLE_CASE_RETURN = (By.XPATH, '//*[@id="case-header-info"]/h4')
    EMPTY_RETURN = 'No'
    SORT = (By.XPATH, '//*[@id="caseSearchResults"]/thead/tr[1]/th[1]')


class ResultRow:

    def __init__(self, county, cookies, row_obj, captcha_solution=None):
        self.county = county
        self.cookies = cookies
        self.captcha_solution = captcha_solution
        self._set_attrs_from_row_obj(row_obj)

    def _set_attrs_from_row_obj(self, row_obj):
        anchor = row_obj.find_element_by_tag_name('a')
        case_detail_url = anchor.get_attribute('href')
        base_url, query_string = case_detail_url.split('?')
        qs = parse_qs(query_string)
        self.case_num = anchor.text
        self.county_num = int(qs['countyNo'][0])

    def case_details(self, use_captcha_solution=False):
        try:
            return self._case_details
        except AttributeError:
            search_api = SearchApi(self.county)
            kwargs = {
                'county_num': self.county_num,
                'cookies': self.cookies,
            }
            if use_captcha_solution:
                kwargs['captcha_solution'] = self.captcha_solution
            case_info = search_api.case_details(self.case_num, **kwargs)
            self._case_details = case_info
            return case_info


class Results(SeleniumHelpers):

    locators = ResultsLocators

    def __init__(self, driver, county, captcha_api_key, captcha_solution=None):
        self.driver = driver
        self.county = county
        self.captcha_api_key = captcha_api_key
        self.captcha_solution = captcha_solution

    def get(self, use_captcha_solution=False):
        """Get case detail data"""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                self.locators.RESULTS_TABLE)
        )
        # Maximize displayed results
        self.click(self.locators.SHOW_ALL_RESULTS)
        # Harvest links on page
        cookies = self.cookies_as_dict()
        rows = self._get_elements_by_locator(self.locators.RESULTS_TABLE_ROWS)
        # Use cookies and harvested Captcha key to make case_detail POST request
        # NOTE: Captcha key only appears to be required on the first request. Strange...
        results = []
        for idx, row in enumerate(rows):
            row_obj = ResultRow(self.county, cookies, row, self.captcha_solution)
            # Only use captcha solution on first case in first daily search result page
            if idx == 0 and use_captcha_solution:
                case_info = row_obj.case_details(use_captcha_solution=True)
            else:
                case_info = row_obj.case_details(use_captcha_solution=False)
            results.append(case_info)
        return results


class SearchResultsPage(SeleniumHelpers):

    locators = ResultsLocators

    def __init__(self, driver, county, captcha_api_key, captcha_solution):
        self.driver = driver
        self.county = county
        self.captcha_api_key = captcha_api_key
        self.captcha_solution = captcha_solution
        self.results = Results(driver, county, captcha_api_key, captcha_solution)
