import shutil
import time

from my_fake_useragent import UserAgent
from retrying import retry
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


## Locators
from selenium.webdriver.common.by import By



class LoginPageLocators:

    USERNAME = (By.ID, 'UserName')
    PASSWORD = (By.ID, 'Password')
    SIGN_IN_BUTTON = (By.CSS_SELECTOR, '.btn.btn-primary')


class PortalPageLocators:

    PORTAL_BUTTONS = (By.CSS_SELECTOR, '.portlet-buttons')


class SearchPageLocators:

    GO_BUTTON = (By.ID, 'submit')
    SEARCH_BOX = (By.CSS_SELECTOR, '#SearchCriteriaContainer input')
    SEARCH_SUBMIT_BUTTON = (By.XPATH, '//*[@id="btnSSSubmit"]')


class SearchResultsPageLocators:

    RESULTS_LIST = (By.CSS_SELECTOR, '#SmartSearchResults')
    NO_RESULTS_MSG = (By.XPATH, '//*[@id="ui-tabs-1"]/div/p')


# Page elements
class SearchBox:

    # locator for search box where search
    # term is entered
    locator = SearchPageLocators.SEARCH_BOX

    def __set__(self, obj, value):
        """Sets the text to the value supplied"""
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(*self.locator)
        )
        driver.find_element(*self.locator).clear()
        driver.find_element(*self.locator).send_keys(value)

    def __get__(self, obj, owner):
        """Gets the text of the specified object"""
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(*self.locator)
        )
        element = driver.find_element(*self.locator)
        return element.get_attribute("value")


class SearchResults:

    locator = (By.CSS_SELECTOR, 'tr.k-detail-row')
    # other possible selectors...
    #  'td.k-detail-cell'
    #  'a.caseLink'

    def __get__(self, obj, owner):
        """Gets the text of the specified object"""
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_elements(*self.locator)
        )
        elements = driver.find_elements(*self.locator)
        #TODO: extract data from elements here
        #return element.get_attribute("value")
        return [1,2,3]

    def _extract_results_metadata(search_results):
        case_rows = search_results['results_el'].find_elements_by_css_selector('tr.k-detail-row')
        case_data = search_results['results_el'].find_elements_by_css_selector('td.k-detail-cell')
        case_links = search_results['results_el'].find_elements_by_css_selector('a.caseLink')
        return case_rows



## Pages
class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def fill_form_field(self, locator_name, value):
        element = self._get_element_by_locator(locator_name)
        element.send_keys(value)

    def click(self, locator_name):
        element = self._get_element_by_locator(locator_name)
        element.click()

    def _get_element_by_locator(self, locator_name):
        locator = getattr(self.locators, locator_name)
        return self.driver.find_element(*locator)


# TODO: Refactor to use FormFieldElement or UsernameField
# and PasswordField (sted of fill_form_field), to
# match the page element strategy used for SearchBox field
# on SearchPage
class LoginPage(BasePage):

    locators = LoginPageLocators

    def __init__(self, driver, url, username, password):
        super().__init__(driver)
        self.username = username
        self.password = password
        self.site_url = url
        base_url = self.site_url.split('Home')[0].rstrip('/')
        self.login_url = base_url + '/Account/Login'

    def go_to(self):
        self.driver.get(self.login_url)

    def login(self):
        self.fill_form_field('USERNAME', self.username)
        self.fill_form_field('PASSWORD', self.password)
        self.click('SIGN_IN_BUTTON')


class PortalPage(BasePage):

    locators = PortalPageLocators

    def go_to_hearings_search(self):
        self._click_port_button('hearings')

    def go_to_smart_search(self):
        self._click_port_button('smart_search')

    def _click_port_button(self, name):
        buttons = self.driver.find_elements(*PortalPageLocators.PORTAL_BUTTONS)
        map = {
            'payments': 0,
            'hearings' : 1,
            'smart_search': 2
        }
        idx = map[name]
        buttons[idx].click()


class SearchPage(BasePage):

    search_box = SearchBox()

    def submit_search(self, timeout=30):
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(
                SearchPageLocators.SEARCH_SUBMIT_BUTTON
            )
        )
        self.driver.find_element(
            *SearchPageLocators.SEARCH_SUBMIT_BUTTON
        ).click()


class SearchResultsPage(BasePage):

    results = SearchResults()

    @retry(
        stop_max_attempt_number=7,
        stop_max_delay=30000,
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000
    )
    def results_found(self):
        try:
            results_el = self.driver.find_element(
                *SearchResultsPageLocators.RESULTS_LIST
            )

            found = True
        except NoSuchElementException:
            pass
        try:
            no_results_el = self.driver.find_element(
                *SearchResultsPageLocators.NO_RESULTS_MSG
            )
        except NoSuchElementException:
            pass
        if results_el and found == True:
            return True
        elif 'No cases match' in no_results.get_attribute('innerText'):
            return False
        else:
            raise Exception("Search not yet completed")


class OdysseySite:

    def __init__(self, url, username, password, download_dir, timeout=60):
        self.site_url = url
        self.username = username
        self.password = password
        self.download_dir = download_dir
        self.timeout = timeout

    def search(self, search_terms, download_assets=False, headless=True):
        failed_searches = []
        results = []
        self.driver = self._init_chrome_driver(headless=headless)
        login_page = LoginPage(
            self.driver,
            self.site_url,
            self.username,
            self.password
        )
        login_page.go_to()
        login_page.login()
        portal_page = PortalPage(self.driver)

        # Instantiate search_page = SearchPge(self.driver)
        # run search for search terms
        data = []
        try:
            for term in search_terms:
                # Conduct search
                search_page = SearchPage(self.driver)
                search_page.search_box = term
                search_page.submit_search(self.timeout)
                results_page = SearchResultsPage(self.driver)
                if results_page.results_found():
                    data.extend(results_page.results)
                """
                # TODO step through detail pages if requested
                try:
                    if download_assets:
                        pass
                        # TODO: step through pages and download assets
                        # Save file assets based on case IDs
                    else:
                        return results
                finally:
                    self.driver.quit()
                """
                #TODO: return to search page
            return data
        finally:
            self.driver.quit()

    def _init_chrome_driver(self, headless=True):
        chrome_options = self._build_chrome_options(headless=headless)
        executable_path = shutil.which('chromedriver')
        driver = webdriver.Chrome(options=chrome_options, executable_path=executable_path)
        return driver

    def _build_chrome_options(self, headless=True):
        # this code alters the browser to download the pdfs
        # it was taken from https://medium.com/@moungpeter/how-to-automate-downloading-files-using-python-selenium-and-headless-chrome-9014f0cdd196
        def enable_download_headless(browser, download_dir):
            browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
            params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
            browser.execute("send_command", params)
        # Options were slightly modified by commenting out things I didn't want
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--verbose')
        chrome_options.add_experimental_option("prefs", {
                "download.default_directory": self.download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing_for_trusted_sources_enabled": False,
                "safebrowsing.enabled": False
        })
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
        ua = UserAgent(family='chrome')
        randomua = ua.random()
        chrome_options.add_argument(f'user-agent={randomua}')
        return chrome_options

    """
    def _search(self, search_term):
        search_results = self._wait_for_search_results(driver)
        if search_results['status'] == 'results found':
            case_metadata = self._extract_results_metadata(driver)
        else:
            return []
            #xpath_query = '/html/body/div[1]/div[2]/div/div[3]/div/div[2]/div/div/div/div/div/div/div/div/div[2]/table/tbody/tr[1]/td[2]/a'
            #driver.find_element_by_xpath(xpath_query).click()

        #WebDriverWait(driver, self.timeout).until(
        #    EC.presence_of_element_located((By.XPATH, '//div[@id="divCaseInformation_header"]'))
        #)

    def _extract_results_metadata(search_results):
        case_rows = search_results['results_el'].find_elements_by_css_selector('tr.k-detail-row')
        case_data = search_results['results_el'].find_elements_by_css_selector('td.k-detail-cell')
        case_links = search_results['results_el'].find_elements_by_css_selector('a.caseLink')
        return case_rows
    """

    # TODO
    def _scrape_case_page(self, driver):
        pass

