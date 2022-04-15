# Scraping tools
# Logging
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from court_scraper.base.selenium_helpers import SeleniumHelpers

logger = logging.getLogger(__name__)


class CaseDetailPageLocators:
    """
    Identifiers for important elements on the case detail page.
    """

    # <FRAME name="main" src="/ESAWebApp/TViewCaseCivil?caseid=06571++OWCR074169&screen=T" scrolling="auto">
    MAIN_FRAME = (By.XPATH, "//frame[@name='main']")


class CaseDetailPage(SeleniumHelpers):
    """
    Interface for interacting with the search results page.
    """

    locators = CaseDetailPageLocators

    def __init__(self, driver):
        self.driver = driver
        self.timeout = 5

    def open(self):
        logger.debug("Opening the case detail page's main frame")
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.locators.MAIN_FRAME)
        )

        # Grab the URL from the frame
        logger.debug("Open the action frame")
        frame = self._get_element_by_locator(self.locators.MAIN_FRAME)
        self.url = frame.get_attribute("src").strip()

        # Go there
        self.driver.get(self.url)
