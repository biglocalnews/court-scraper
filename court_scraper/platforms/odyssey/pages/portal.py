from selenium.webdriver.common.by import By

from .base import BasePage


class PortalPageLocators:

    PORTAL_BUTTONS = (By.CSS_SELECTOR, '.portlet-buttons')
    IMAGES = (By.TAG_NAME, 'img')


class PortalPage(BasePage):

    locators = PortalPageLocators

    @property
    def is_current_page(self):
        return len(
            self.driver.find_elements(*self.locators.PORTAL_BUTTONS)
        ) > 0

    def go_to_hearings_search(self):
        self._click_port_button('hearings')

    def go_to_smart_search(self):
        self._click_port_button('smart_search')

    def _click_port_button(self, name):
        images = self.driver.find_elements(*self.locators.IMAGES)
        img_names = {
            'hearings': 'Icon_SearchHearing.svg',
            'smart_search': 'Icon_SmartSearch.svg'
        }
        image_name = img_names['smart_search']
        button = None
        for img in images:
            src = img.get_attribute('src')
            if src.endswith(image_name):
                # If image matches, get parent anchor tag
                button = img.find_element_by_xpath('..')
                break
        button.click()
