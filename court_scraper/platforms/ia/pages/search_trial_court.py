# Scraping tools
# Logging
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from court_scraper.base.selenium_helpers import SeleniumHelpers
from court_scraper.captcha import resolve_recaptcha_v2

logger = logging.getLogger(__name__)


class SearchTrialCourtPageLocators:
    """
    Identifiers for important elements on the trial court search page.
    """

    # <FRAME name="main" src='/ESAWebApp/TrialCourtStateWide' scrolling="auto">
    FORM_FRAME = (By.XPATH, "//frame[@src='/ESAWebApp/TrialCourtStateWide']")

    # <a href="#caseidSearch" class="ui-tabs-anchor" role="presentation" ...
    CASE_ID_TAB = (By.XPATH, "//a[@href='#caseidSearch']")

    # <select name="caseid1sel" title="caseid1sel" onchange="countysel(this.form)" tabindex="200">
    COUNTY_SELECT = (By.XPATH, "//select[@name='caseid1sel']")

    # <select name="caseid3sel" title="caseid3sel" onchange="casetypesel(this.form)" tabindex="201">
    CASE_TYPE_SELECT = (By.XPATH, "//select[@name='caseid3sel']")

    # <input type="Text" name="caseid4" size="8" tabindex="204">
    CASE_ID_INPUT = (By.XPATH, "//input[@name='caseid4']")

    # <input type="Submit" name="search" value="Search" onclick="...
    SEARCH_BUTTON = (By.XPATH, "//input[@name='search']")


class SearchTrialCourtPage(SeleniumHelpers):
    """
    Interface for interacting with the trail court search page.
    """

    locators = SearchTrialCourtPageLocators
    url = "https://www.iowacourts.state.ia.us/ESAWebApp/TrialSimpFrame"

    def __init__(self, driver):
        self.driver = driver
        self.timeout = 5

    def _open_form_frame(self):
        """
        Open the private frame where the form is hiding.
        """
        logger.debug("Waiting for the form frame")
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.locators.FORM_FRAME)
        )

        logger.debug("Open the form frame")
        url = "https://www.iowacourts.state.ia.us/ESAWebApp/TrialCourtStateWide"
        self.driver.get(url)

        logger.debug("Waiting for the tabs")
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.locators.CASE_ID_TAB)
        )

    def open_case_number_search_tab(self):
        """
        Switch to the 'Case ID Search' tab
        """
        # Open the frame where the form is hiding
        self._open_form_frame()

        # Click into the trial court search
        logger.debug("Clicking the case number search tab")
        self.click(self.locators.CASE_ID_TAB)

    @resolve_recaptcha_v2
    def search_for_case_by_number(self, county_id, case_type, case_id):
        """
        Fill out the search form and search for a case.
        """
        # Pick the county from the form
        logger.debug(f"Selecting county: {county_id}")
        self.select_form_field(self.locators.COUNTY_SELECT, county_id)

        # Pick the case_type from the form
        logger.debug(f"Selecting case type: {case_type}")
        self.select_form_field(self.locators.CASE_TYPE_SELECT, case_type)

        # Enter the case_id into the form
        logger.debug(f"Entering case id: {case_id}")
        self.fill_form_field(self.locators.CASE_ID_INPUT, case_id)

        # Once it's ready, hit the submit button
        logger.debug("Hitting the submit button")
        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(
                self.locators.SEARCH_BUTTON,
            )
        )
        self.click(self.locators.SEARCH_BUTTON)

        # Switch to the search results tab
        logger.debug("Switch to the results tab")
        self.driver.switch_to.window(self.driver.window_handles[-1])
