from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .base import BasePage


class CaseDetailPageLocators:

    FINANCIAL_INFO = (
        By.CSS_SELECTOR,
        'div#divFinancialInformation_body h1'
    )

class CaseDetailPage(BasePage):

    financials_locator = CaseDetailPageLocators.FINANCIAL_INFO

    @property
    def page_source(self):
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element(
                self.financials_locator,
                'Financial'
            )
        )
        return self.driver.page_source

