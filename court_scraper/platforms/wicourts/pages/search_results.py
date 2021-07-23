from urllib.parse import parse_qs

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from court_scraper.case_info import CaseInfo
from court_scraper.base.selenium_helpers import SeleniumHelpers


class ResultsLocators:

    SHOW_ALL_RESULTS = (By.XPATH, '//*[@id="caseSearchResults_length"]/label/select/option[5]')
    RESULTS_TABLE_ROWS = (By.XPATH, '//*[@id="caseSearchResults"]/tbody/tr')
    RESULTS_TABLE = (By.XPATH, '//*[@id="caseSearchResults"]')
    YEAR_FILTER = (By.XPATH, '//*[@id="caseSearchResults"]/thead/tr[2]/td[1]/input')
    SINGLE_CASE_RETURN = (By.XPATH, '//*[@id="case-header-info"]/h4')
    EMPTY_RETURN = 'No'
    SORT = (By.XPATH, '//*[@id="caseSearchResults"]/thead/tr[1]/th[1]')


class ResultRow:

    def __init__(self, cookies, row_obj, captcha_solution=None):
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
            data = self._get_case_details(use_captcha_solution=use_captcha_solution)
            self._case_details = data
            return data

    def _get_case_details(self, use_captcha_solution=False):
        # {"countyNo":40,"caseNo":"2021TW002317"}
        payload = {
            'countyNo': self.county_num,
            'caseNo': self.case_num,
        }
        if use_captcha_solution:
            payload['captcha'] = f'{{"hcaptcha":"{self.captcha_solution}"}}'
        with requests.Session() as session:
            response = session.post(
                'https://wcca.wicourts.gov/jsonPost/caseDetail',
                json=payload,
                cookies=self.cookies
            )
        return response.json()


class Results(SeleniumHelpers):

    locators = ResultsLocators

    def __init__(self, driver, captcha_api_key, captcha_solution=None):
        self.driver = driver
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
        cookies = {cookie['name']:cookie['value'] for cookie in self.driver.get_cookies()}
        rows = self._get_elements_by_locator(self.locators.RESULTS_TABLE_ROWS)
        # Use cookies and harvested Captcha key to make case_detail POST request
        # NOTE: Captcha key only appears to be required on the first request. Strange...
        results = []
        CaseInfoMapped = self._get_case_info_mapped_class()
        for idx, row in enumerate(rows):
            row_obj = ResultRow(cookies, row, self.captcha_solution)
            # Only use captcha solution on first case in first daily search result page
            if idx == 0 and use_captcha_solution:
                data = row_obj.case_details(use_captcha_solution=True)
            else:
                data = row_obj.case_details(use_captcha_solution=False)
            case_info = CaseInfoMapped(data)
            results.append(data['result'])
        return results


    def _get_case_info_mapped_class(self):
        mapping = {
            'caseNo': 'number',
            'civilJdgmts': 'civil_judgements',
            'filingDate': 'filing_date',
            'wcisClsCode': 'wcis_code',
            'crossReferenced': 'cross_referenced',
            'countyNo': 'county_num',
            'countyName': 'county',
            'isCriminal': 'is_criminal',
            'isReopenedRemandedFromAppeal': 'is_reopened_remanded_from_appeal',
            'classType': 'type',
            'caseType': 'type_code',
            'prosAgency': 'prosecuting_agency',
            'defAttys': 'def_attys',
        }
        CaseInfo._map = mapping
        return CaseInfo


class SearchResultsPage(SeleniumHelpers):

    locators = ResultsLocators

    def __init__(self, driver, captcha_api_key, captcha_solution):
        self.driver = driver
        self.captcha_api_key = captcha_api_key
        self.captcha_solution = captcha_solution
        self.results = Results(driver, captcha_api_key, captcha_solution)

    def results_found(self):
        # TODO
        pass

    def display_max_results(self):
        # TODO
        pass
