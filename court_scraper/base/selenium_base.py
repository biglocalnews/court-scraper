from selenium.webdriver.common.keys import Keys

class SeleniumPage:

    def __init__(self, driver):
        self.driver = driver

    def fill_form_field(self, locator_name, value):
        element = self._get_element_by_locator(locator_name)
        element.send_keys(value + Keys.RETURN)
    
    def click(self, locator_name):
        element = self._get_element_by_locator(locator_name)
        element.click()

    def _get_element_by_locator(self, locator_name):
        return self.driver.find_element(*locator_name)
    
    def _get_elements_by_locator(self, locator_name):
        return self.driver.find_elements(*locator_name)