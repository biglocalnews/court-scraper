from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .base import BasePage
from court_scraper.captcha import resolve_recaptcha_v2


# Locators
class SearchPageLocators:

    GO_BUTTON = (By.ID, 'submit')
    SEARCH_BOX = (By.CSS_SELECTOR, '#SearchCriteriaContainer input')
    SEARCH_SUBMIT_BUTTON = (By.XPATH, '//*[@id="btnSSSubmit"]')


# Elements
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
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(*self.locator)
        )
        element = driver.find_element(*self.locator)
        return element.get_attribute("value")


class SearchPage(BasePage):

    search_box = SearchBox()

    @resolve_recaptcha_v2
    def submit_search(self, timeout=30):
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(
                SearchPageLocators.SEARCH_SUBMIT_BUTTON
            )
        )
        self.driver.find_element(
            *SearchPageLocators.SEARCH_SUBMIT_BUTTON
        ).click()
