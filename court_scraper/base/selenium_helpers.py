from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class SeleniumHelpers:
    def go_to(self, url=None):
        """
        Go to the provided URL.
        """
        target_url = url or self.url
        self.driver.get(target_url)

    def fill_form_field(self, locator_name, value):
        """
        Enters the provided value into a HTML form input.
        """
        element = self._get_element_by_locator(locator_name)
        element.send_keys(value)

    def select_form_field(self, locator_name, value):
        """
        Select an <option> from an HTML <select> form input.
        """
        element = self._get_element_by_locator(locator_name)
        select = Select(element)
        select.select_by_value(value)

    def click(self, locator_name):
        """
        Click on an element.
        """
        element = self._get_element_by_locator(locator_name)
        element.click()

    def enter(self, locator_name):
        """
        Select an element and hit the enter key.
        """
        element = self._get_element_by_locator(locator_name)
        element.send_keys(Keys.RETURN)

    def _get_element_by_locator(self, locator_name):
        """
        Returns the element with the provided locator.
        """
        return self.driver.find_element(*locator_name)

    def _get_elements_by_locator(self, locator_name):
        """
        Returns a list of elements with the provided locator.
        """
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
