from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from base.selenium_base import BasePage

# Locators
class SearchPageLocators:

    COUNTY_SELECT = (By.ID, 'db')
    SEARCH_BOX = (By.ID, 'number')
    GO_BUTTON = (By.XPATH, '//input[@type="submit"]')
    
# Elements

class SearchBox:

    # locator for search box where search
    # term is entered
    county_locator = SearchPageLocators.COUNTY_SELECT
    search_locator = SearchPageLocators.SEARCH_BOX
    go_locator = SearchPageLocators.GO_BUTTON

    #this sets the supplied value
    def __set__(self, obj, value):
        """Sets the text to the value supplied"""
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(*self.search_locator)
        )
        driver.find_element(*self.county_locator).send_keys(county)
        driver.find_element(*self.search_locator).send_keys(value)
        
    #this returns the input value
    def __get__(self, obj, owner):
        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(*self.go_locator)
        )
        element = driver.find_element(*self.go_locator)
        return element.get_attribute("value")
        


class SearchPage(BasePage):

    search_box = SearchBox()

    def submit_search(self, timeout=30):
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(
                SearchPageLocators.GO_BUTTON
            )
        )
        self.driver.find_element(
            *SearchPageLocators.GO_BUTTON
        ).click()
