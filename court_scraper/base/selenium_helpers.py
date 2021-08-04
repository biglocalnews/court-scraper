from selenium.webdriver.common.keys import Keys


class SeleniumHelpers:

    def go_to(self, url=None):
        target_url = url or self.url
        self.driver.get(target_url)

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

    def cookies_as_dict(self):
        return {cookie['name']: cookie['value'] for cookie in self.driver.get_cookies()}
