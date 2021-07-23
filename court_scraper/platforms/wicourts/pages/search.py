from urllib.parse import parse_qs

from anticaptchaofficial.hcaptchaproxyless import hCaptchaProxyless
from selenium.webdriver.common.by import By

from court_scraper.base.selenium_helpers import SeleniumHelpers
from court_scraper.utils import dates_for_range
from .search_results import SearchResultsPage
from ..captcha import CaptchaHelpers


class SearchLocators:
    LAST_NAME = (By.NAME, 'lastName')
    FIRST_NAME = (By.NAME, 'firstName')
    MIDDLE_NAME = (By.NAME, 'middleName')
    BIRTH_DATE = (By.NAME, 'dateOfBirth')
    BUSINESS_NAME = (By.NAME, 'businessName')
    COUNTY = (By.XPATH,'//*[@id="react-select-2--value"]/div[2]/input')
    CASE_NUMBER = (By.NAME, 'caseNo')
    CASE_NUMBER_RANGE_YEAR = (By.XPATH, '//*[@id="react-select-3--value"]/div[2]/input')
    CASE_NUMBER_RANGE_TYPE = (By.XPATH, '//*[@id="react-select-4--value"]/div[2]/input')
    CASE_NUMBER_RANGE_BEGIN = (By.NAME, 'caseNoRange.start')
    CASE_NUMBER_RANGE_END = (By.NAME, 'caseNoRange.end')
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


class SearchPage(CaptchaHelpers, SeleniumHelpers):

    search = SearchLocators()

    def __init__(self, driver, captcha_api_key=None):
        self.url = "https://wcca.wicourts.gov/advanced.html"
        self.captcha_api_key = captcha_api_key
        self.driver = driver

    def search_by_date(self, county, start_date, end_date, case_type=None):
        date_format = "%m-%d-%Y"
        dates = dates_for_range(start_date, end_date, output_format=date_format)
        payload = []
        for idx, day in enumerate(dates):
            self.go_to() # advanced search page
            self._execute_search(county, day, day, case_type)
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
            results_page = SearchResultsPage(self.driver, self.captcha_api_key, captcha_solution)
            results = results_page.results.get(**result_kwargs)
            # TODO: if results_page.results_found():
            #    results_page.display_max_results()
            payload.extend(results)
        return payload

    def _execute_search(self, county, start_date, end_date, case_type=None, captcha_solution=None):
        self.fill_form_field(self.search.COUNTY, county)
        self.fill_form_field(self.search.FILING_DATE_RANGE_BEGIN, start_date)
        self.fill_form_field(self.search.FILING_DATE_RANGE_END, end_date)
        # TODO: support multiple case types
        if case_type:
            self.fill_form_field(self.search.DATE_CASE_TYPE, case_type)
        self.click(self.search.SEARCH_BUTTON)

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
