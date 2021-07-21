from urllib.parse import parse_qs

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from court_scraper.base.selenium_helpers import SeleniumHelpers
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

class ResultsLocators:

    SHOW_ALL_RESULTS = (By.XPATH, '//*[@id="caseSearchResults_length"]/label/select/option[5]')
    RESULTS_TABLE_ROWS = (By.XPATH, '//*[@id="caseSearchResults"]/tbody/tr')
    RESULTS_TABLE = (By.XPATH, '//*[@id="caseSearchResults"]')
    YEAR_FILTER = (By.XPATH, '//*[@id="caseSearchResults"]/thead/tr[2]/td[1]/input')
    SINGLE_CASE_RETURN = (By.XPATH, '//*[@id="case-header-info"]/h4')
    EMPTY_RETURN = 'No'
    SORT = (By.XPATH, '//*[@id="caseSearchResults"]/thead/tr[1]/th[1]')


class SearchPage(CaptchaHelpers, SeleniumHelpers):

    search = SearchLocators()
    results = ResultsLocators()

    def __init__(self, driver):
        self.url = "https://wcca.wicourts.gov/advanced.html"
        self.driver = driver

    def search_by_date(self, county, start_date, end_date, case_type=None):
        self.go_to()
        self.fill_form_field(self.search.COUNTY, county)
        self.fill_form_field(self.search.FILING_DATE_RANGE_BEGIN, start_date)
        self.fill_form_field(self.search.FILING_DATE_RANGE_END, end_date)
        if case_type:
            self.fill_form_field(self.search.DATE_CASE_TYPE, case_type)
        self.click(self.search.SEARCH_BUTTON)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                self.results.RESULTS_TABLE)
        )
        # TODO: May need to test page for presence of captcha
        # TODO: Ensure results expansion works
        try:
            self.click(self.results.SHOW_ALL_RESULTS)
        except:
            pass
        # Harvest links on page
        rows = self._get_elements_by_locator(self.results.RESULTS_TABLE_ROWS)
        #  Click on the first case link to trigger and solve the captcha
        first_link = rows[0].find_element_by_tag_name('a')
        first_link.click()
        g_response = self._solve_captcha(self.driver)
        # Move back to original search results page
        self.driver.back()
        cookies = {cookie['name']:cookie['value'] for cookie in self.driver.get_cookies()}
        # Refresh the row elements
        rows = self._get_elements_by_locator(self.results.RESULTS_TABLE_ROWS)
        # Use cookies and harvested Captcha key to make case_detail POST request
        # NOTE: Captcha key only appears to be required on the first request. Strange...
        results = []
        for idx, row in enumerate(rows):
            if idx == 0:
                data = self._get_case_details(cookies, row, g_response)
            else:
                data = self._get_case_details(cookies, row)
            results.append(data['result'])
        return results

    def _get_case_details(self, cookies, row, captcha_key=None):
        #{"countyNo":40,"caseNo":"2021TW002317"}
        anchor = row.find_element_by_tag_name('a')
        case_num = anchor.text
        case_detail_url = anchor.get_attribute('href')
        base_url, query_string = case_detail_url.split('?')
        qs = parse_qs(query_string)
        payload = {
            'countyNo': int(qs['countyNo'][0]),
            'caseNo': case_num,
        }
        if captcha_key:
            payload['captcha'] = f'{{"hcaptcha":"{captcha_key}"}}'
        with requests.Session() as session:
            response = session.post(
                'https://wcca.wicourts.gov/jsonPost/caseDetail',
                json=payload,
                cookies=cookies
            )

        return response.json()

    def _solve_captcha(self, driver):
        from anticaptchaofficial.hcaptchaproxyless import hCaptchaProxyless
        #iframe = driver.find_element_by_tag_name('iframe')
        iframe = None
        for frame in self.driver.find_elements_by_tag_name('iframe'):
            if 'challenge' in frame.get_attribute('src'):
                iframe = frame
                break
        iframe_url = iframe.get_attribute('src')
        query_str = iframe_url.split('#')[-1]
        site_key = parse_qs(query_str)['sitekey'][0]
        #site_key = 'd99012c0-7c0c-4575-9f8f-962ee8cdca65'
        captcha_id = iframe.get_attribute('data-hcaptcha-widget-id')
        text_area_id = f"g-recaptcha-response-{captcha_id}"
        # TODO: configure API key upstream and/or pass in
        api_key = "YOUR API KEY"
        solver = hCaptchaProxyless()
        solver.set_verbose(1)
        solver.set_key(api_key)
        solver.set_website_url(driver.current_url)
        solver.set_website_key(site_key)
        g_response = solver.solve_and_return_solution()
        return g_response
