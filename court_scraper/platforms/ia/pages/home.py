# Scraping tools
# Logging
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from court_scraper.base.selenium_helpers import SeleniumHelpers

logger = logging.getLogger(__name__)


class HomePageLocators:
    """
    Identifiers for important elements on the home page.
    """

    LINK = (By.XPATH, "//a")


class HomePage(SeleniumHelpers):
    """
    Interface for interacting with the home page.
    """

    locators = HomePageLocators
    url = "https://www.iowacourts.state.ia.us/ESAWebApp/DefaultFrame?in=1"

    def __init__(self, driver):
        self.driver = driver
        self.timeout = 5

    def open(self):
        """
        Open the homepage.
        """
        logger.debug("Opening Iowa home page")
        self.driver.get(self.url)
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.locators.LINK)
        )
        logger.debug("Iowa home page ready")

    def start_search(self):
        """
        Click the "start search" button to access the input forms.
        """
        logger.debug("Clicking the start search link")
        self.click(self.locators.LINK)
