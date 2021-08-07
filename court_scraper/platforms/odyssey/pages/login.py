from selenium.webdriver.common.by import By

from .base import BasePage


class LoginPageLocators:

    USERNAME = (By.ID, 'UserName')
    PASSWORD = (By.ID, 'Password')
    SIGN_IN_BUTTON = (By.CSS_SELECTOR, '.btn.btn-primary')


# TODO: Refactor to use FormFieldElement or UsernameField
# and PasswordField (sted of fill_form_field), to
# match the page element strategy used for SearchBox field
# on SearchPage
class LoginPage(BasePage):

    locators = LoginPageLocators

    def __init__(self, driver, url, username, password):
        super().__init__(driver)
        self.username = username
        self.password = password
        self.site_url = url
        base_url = self.site_url.split('Home')[0].rstrip('/')
        self.login_url = base_url + '/Account/Login'

    def go_to(self):
        self.driver.get(self.login_url)

    def login(self):
        self.fill_form_field('USERNAME', self.username)
        self.fill_form_field('PASSWORD', self.password)
        self.click('SIGN_IN_BUTTON')
