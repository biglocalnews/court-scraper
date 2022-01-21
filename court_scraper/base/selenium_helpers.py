from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class SeleniumHelpers:
    def go_to(self, url=None):
        target_url = url or self.url
        self.driver.get(target_url)

    def fill_form_field(self, locator_name, value):
        element = self._get_element_by_locator(locator_name)
        element.send_keys(value + Keys.RETURN)

    def select_form_field(self, locator_name, value):
        element = self._get_element_by_locator(locator_name)
        select = Select(element)
        select.select_by_value(value)

    def click(self, locator_name):
        element = self._get_element_by_locator(locator_name)
        element.click()

    def _get_element_by_locator(self, locator_name):
        return self.driver.find_element(*locator_name)

    def _get_elements_by_locator(self, locator_name):
        return self.driver.find_elements(*locator_name)

    def cookies_as_dict(self):
        return {cookie["name"]: cookie["value"] for cookie in self.driver.get_cookies()}

    def wait_until_clickable(self, locator_name, timeout=10, driver=None):
        """
        Pause until the provided locator is clickable to continue.
        """
        if driver:
            d = driver
        else:
            d = self.driver
        WebDriverWait(d, timeout).until(EC.element_to_be_clickable(locator_name))

    def wait_until_visible(self, locator_name, timeout=10, driver=None):
        """
        Pause until the provided locator is visible to continue.
        """
        if driver:
            d = driver
        else:
            d = self.driver
        WebDriverWait(d, timeout).until(EC.visibility_of_element_located(locator_name))
