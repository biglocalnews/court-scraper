from urllib.parse import parse_qs

from anticaptchaofficial.hcaptchaproxyless import hCaptchaProxyless
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from court_scraper.base.selenium_helpers import SeleniumHelpers
from court_scraper.utils import dates_for_range
from .search_results import SearchResultsPage
from ..search_api import SearchApi


class SearchLocators:
    LAST_NAME = (By.NAME, 'lastName')
    FIRST_NAME = (By.NAME, 'firstName')
    MIDDLE_NAME = (By.NAME, 'middleName')
    BIRTH_DATE = (By.NAME, 'dateOfBirth')
    BUSINESS_NAME = (By.NAME, 'businessName')
    COUNTY = (By.XPATH, '//*[@id="react-select-2--value"]/div[2]/input')
    COUNTY_DROPDOWN_ARROW = (By.CSS_SELECTOR, '.Select-arrow-zone')
    CASE_NUMBER = (By.NAME, 'caseNo')
    CASE_NUMBER_RANGE_YEAR = (By.XPATH, '//*[@id="react-select-3--value"]/div[2]/input')
    CASE_NUMBER_RANGE_TYPE = (By.XPATH, '//*[@id="react-select-4--value"]/div[2]/input')
    CASE_NUMBER_RANGE_BEGIN = (By.NAME, 'caseNoRange.start')
    CASE_NUMBER_RANGE_END = (By.NAME, 'caseNoRange.end')
    CASE_RESULTS_TABLE = (By.CSS_SELECTOR, 'table#caseSearchResults')
    DATE_CASE_TYPE = (By.XPATH, '//*[@id="react-select-5--value"]/div[2]/input')
    DATE_CASE_STATUS = (By.XPATH, '//*[@id="react-select-6--value"]/div[2]/input')
    FILING_DATE_RANGE_BEGIN = (By.NAME, 'filingDate.start')
    FILING_DATE_RANGE_END = (By.NAME, 'filingDate.end')
    DISPOSITION_DATE_RANGE_BEGIN = (By.NAME, 'dispositionDate.start')
    DISPOSITION_DATE_RANGE_END = (By.NAME, 'dispositionDate.end')
    STATE_BAR_ID = (By.NAME, 'attyNo')
    CITATION_NUMBER = (By.NAME, 'citnNo')
    DA_CASE_NUMBER = (By.NAME, 'daCaseNo')
    ISSUING_AGENCY = (By.XPATH, '//*[@id="react-select-8--value"]/div[2]/input')
    OFFENSE_DATE_BEGIN = (By.NAME, 'offenseDate.start')
    OFFENSE_DATE_END = (By.NAME, 'offenseDate.end')
    SEARCH_BUTTON = (By.NAME, 'search')
    RESET_BUTTON = (By.XPATH, '//*[@id="home-container"]/main/div/form/div[11]/div/button[2]')


class SearchPage(SeleniumHelpers):

    locators = SearchLocators

    def __init__(self, driver, captcha_api_key=None):
        self.url = "https://wcca.wicourts.gov/advanced.html"
        self.captcha_api_key = captcha_api_key
        self.driver = driver

    def search_by_case_number(self, county, case_numbers=[]):
        payload = []
        search_api = SearchApi(county)
        for idx, case_num in enumerate(case_numbers):
            self.go_to()  # advanced search page
            self._execute_case_search(county, case_num)
            # Solve and apply the captcha on the first search.
            # (using it on subsequent case detail API calls causes errors)
            kwargs = {
                'cookies': self.cookies_as_dict(),
            }
            if idx == 0:
                kwargs['captcha_solution'] = self.solve_captcha()
            case_info = search_api.case_details(case_num, **kwargs)
            payload.append(case_info)
        return payload

    def search_by_date(self, county, start_date, end_date, case_types=[]):
        date_format = "%m-%d-%Y"
        dates = dates_for_range(start_date, end_date, output_format=date_format)
        payload = []
        for idx, day in enumerate(dates):
            self.go_to()  # advanced search page
            self._execute_date_search(county, day, day, case_types)
            if not self.search_has_results(self.driver.current_url):
                continue
            # Solve the captcha on the first search,
            # save the solution for re-use, and apply the solution
            # on the first case of the first day's search results
            # (using it on subsequent case detail API calls causes errors)
            result_kwargs = {
                'use_captcha_solution': False
            }
            if idx == 0:
                captcha_solution = self.solve_captcha()
                result_kwargs['use_captcha_solution'] = True
            # Searches that yield a single result redirect automatically
            # to case detail page rather than search results listing page.
            # For these cases, immediately execute the case detail query
            if 'caseDetail' in self.driver.current_url:
                case_info = self._get_case_details(
                    county,
                    self.driver.current_url,
                    captcha_solution,
                    result_kwargs['use_captcha_solution']
                )
                results = [case_info]
            else:
                results_page = SearchResultsPage(self.driver, county, self.captcha_api_key, captcha_solution)
                results = results_page.results.get(**result_kwargs)
            # TODO: if results_page.results_found():
            #    results_page.display_max_results()
            payload.extend(results)
        return payload

    def _get_case_details(self, county, url, captcha_solution, use_captcha_solution):
        # caseNo=2021SC000082&countyNo=2
        query_str = url.split('?')[-1]
        param_strs = query_str.split('&')
        params = {}
        for param_pair in param_strs:
            key, val = param_pair.split('=')
            params[key] = val
        case_num = params['caseNo']
        search_api = SearchApi(county)
        kwargs = {
            'cookies': self.cookies_as_dict(),
            'county_num': int(params['countyNo'])
        }
        if use_captcha_solution:
            kwargs['captcha_solution'] = captcha_solution
        return search_api.case_details(case_num, **kwargs)

    def _execute_case_search(self, county, case_number):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                self.locators.COUNTY
            )
        )
        clean_county = self._county_titlecase(county)
        self.fill_form_field(self.locators.COUNTY, clean_county)
        self.fill_form_field(self.locators.CASE_NUMBER, case_number)
        self.click(self.locators.SEARCH_BUTTON)

    def _execute_date_search(self, county, start_date, end_date, case_types=[]):
        # Wait until the county dropdown-menu arrow is clickable before filling the form field,
        # in order to avoid overwriting of the field value by the "Statewide" option default
        county_label_obj = self.driver.find_element_by_xpath("//label[contains(text(), 'County')]")
        WebDriverWait(county_label_obj, 10).until(
            EC.element_to_be_clickable(
                self.locators.COUNTY_DROPDOWN_ARROW
            )

        )
        clean_county = self._county_titlecase(county)
        self.fill_form_field(self.locators.COUNTY, clean_county)
        self.fill_form_field(self.locators.FILING_DATE_RANGE_BEGIN, start_date)
        self.fill_form_field(self.locators.FILING_DATE_RANGE_END, end_date)
        if case_types:
            self._select_case_types(case_types)
        self.click(self.locators.SEARCH_BUTTON)

    def _county_titlecase(self, county):
        return county.replace('_', ' ').title()

    def _select_case_types(self, case_types):
        # TODO: Refactor to use locators
        for case_type in case_types:
            # Locate the case type menu by name
            case_type_label_obj = self.driver.find_element_by_xpath("//label[contains(text(), 'Case types')]")
            # Expand the Case types menu
            select_arrow = case_type_label_obj.find_element_by_css_selector('.Select-arrow-zone')
            select_arrow.click()
            # Find and click the selection menu option for the case type
            option_divs = (
                case_type_label_obj
                .find_element_by_css_selector('.Select-menu')
                .find_elements_by_tag_name('div')
            )
            option = [opt for opt in option_divs if opt.text.endswith(f'({case_type})')][0]
            option.click()

    def solve_captcha(self):
        # Solve the captcha
        iframe = None
        for frame in self.driver.find_elements_by_tag_name('iframe'):
            if 'challenge' in frame.get_attribute('src'):
                iframe = frame
                break
        iframe_url = iframe.get_attribute('src')
        query_str = iframe_url.split('#')[-1]
        site_key = parse_qs(query_str)['sitekey'][0]
        solver = hCaptchaProxyless()
        solver.set_verbose(1)
        solver.set_key(self.captcha_api_key)
        solver.set_website_url(self.driver.current_url)
        solver.set_website_key(site_key)
        g_response = solver.solve_and_return_solution()
        return g_response

    def search_has_results(self, current_url):
        WebDriverWait(self.driver, 10).until(
            EC.url_changes(current_url)
        )
        # Return True if it's a single-result redirect to case detail page
        if 'caseDetail' in self.driver.current_url:
            return True
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                self.locators.CASE_RESULTS_TABLE
            )
        )
        if 'No records found' in self.driver.page_source:
            return False
        else:
            # Otherwise, assume there are results
            return True
