from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .base import BasePage


class CaseDetailPageLocators:

    SIDENAV_CASE_INFO_LINK = (
        By.XPATH,
        '//a[text()="Case Information"]'
    )


class CaseDetailPage(BasePage):

    sidenav_case_info_locator = CaseDetailPageLocators.SIDENAV_CASE_INFO_LINK

    @property
    def page_source(self):
        """
        Page source waits for Case Info to appear
        in sidebar nav before proceeding.

        This strategy may not be robust enough
        to handle long-loading page sections.

        See NOTE below for beginnings of an alternative
        strategy.
        """
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.sidenav_case_info_locator)
        )
        """
        # NOTE: Below are some initial thoughts on an alternate
        strategy to wait for page load, if the more naive approach
        above doesn't work consistently for pages with longer-loading
        h1 sections.

        # Grab the section heads from sidebar nav
        side_nav = self.driver.find_element(*self.sidenav_locator)
        section_heads = [
            a.get_attribute('text') for a in
            side_nav.find_elements_by_tag_name('a')
        ]
        # TODO: Feed section_heads into an XPATH query that
        uses presence_of_all_elements? Or if XPATH/presence method
        don't support this, may need more a custom wait
        condition (https://selenium-python.readthedocs.io/waits.html)
        or some other approach

        # Example of finding h1 element that could be long-loading
        self.driver.find_elements_by_xpath('//h1[text()="Documents"]')
        """
        return self.driver.page_source
