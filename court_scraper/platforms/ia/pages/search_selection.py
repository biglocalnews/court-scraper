# Scraping tools
# Logging
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from court_scraper.base.selenium_helpers import SeleniumHelpers

logger = logging.getLogger(__name__)


class SearchSelectionPageLocators:
    """
    Identifiers for important elements on the search selection page.
    """

    # <frame name="main" src="/ESAWebApp/SelectAction" scrolling="auto">
    ACTION_FRAME = (By.XPATH, "//frame[@src='/ESAWebApp/SelectAction']")

    # <a href="/ESAWebApp/TrialSimpFrame" target="_top"><font size="4">Case Search</font></a>
    TRIAL_COURT_SEARCH = (By.XPATH, "//a[@href='/ESAWebApp/TrialSimpFrame']")


class SearchSelectionPage(SeleniumHelpers):
    """
    Interface for interacting with the search selection page.
    """

    locators = SearchSelectionPageLocators
    url = "https://www.iowacourts.state.ia.us/ESAWebApp/SelectFrame"

    def __init__(self, driver):
        self.driver = driver
        self.timeout = 5

    def _open_selection_frame(self):
        """
        Open the private frame where the form is hiding.
        """
        logger.debug("Waiting for the action frame")
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.locators.ACTION_FRAME)
        )

        logger.debug("Open the action frame")
        url = "https://www.iowacourts.state.ia.us/ESAWebApp/SelectAction"
        self.driver.get(url)

        logger.debug("Waiting for the search links")
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.locators.TRIAL_COURT_SEARCH)
        )

    def open_appellate_court_search(self):
        """
        Click into the appellate court search page
        """
        raise NotImplementedError

    def open_trial_court_search(self):
        """
        Click into the trial court search page
        """
        # Open the frame with the search links
        self._open_selection_frame()

        # Click into the trial court search
        logger.debug("Clicking the trial court search link")
        self.click(self.locators.TRIAL_COURT_SEARCH)
