from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base_page import WisconsinBasePage
from court_scraper.base.search_page_mixin import SearchPageMixIn
from court_scraper.captcha.invisible_recaptcha_v2 import InvisibleRecaptchaV2
from captcha import CaptchaLocators
from url import URLs

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

class SearchPage(WisconsinBasePage, SearchPageMixIn):
    
    search = SearchLocators()
    results = ResultsLocators()
    urls = WisconsinURLs()

    def _county_specific_selenium_steps(self):
        self.go_to()
        self.fill_form_field(self.search.COUNTY, self.county)
        self.fill_form_field(self.search.FILING_DATE_RANGE_BEGIN, self.url_date)
        self.fill_form_field(self.search.FILING_DATE_RANGE_END, self.url_date)
        self.fill_form_field(self.search.DATE_CASE_TYPE, self.case_prefix)
        self.click(self.search.SEARCH_BUTTON)
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    self.results.RESULTS_TABLE)
            )
        except:
            self.test_captcha()
            self.solve_captcha()
        try:
            self.click(self.results.SHOW_ALL_RESULTS)
        except:
            pass
        time.sleep(.2)
        self.click(self.results.SORT)
        time.sleep(.2)
        if test_driver.find_element(*self.results.SORT).get_attribute('aria-sort') == 'descending':
            self.click(self.results.SORT)
        else:
            pass
        time.sleep(.2)
        self.fill_form_field(self.results.YEAR_FILTER, str(self.year))
        
    def most_recent_case(self, county, year, case_prefix, session=None, driver=None, row_locator=None, single_case_locator=None):
        return super().most_recent_case(county, year, case_prefix, session=None, driver=self.driver, row_locator=self.results.RESULTS_TABLE_ROWS, single_case_locator=self.results.SINGLE_CASE_RETURN, empty_return_text=self.results.EMPTY_RETURN)