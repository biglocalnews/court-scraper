from anticaptchaofficial.recaptchav2proxyless import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

from .recaptcha import Recaptcha

class InvisibleRecaptchaV2(Recaptcha):
        
    # this function actually gets captcha response and injuects via callback function
    def _inject_response(self):
        self.driver.execute_script(f'{self.callback_function}("{self.g_response}")')

    #this function creates a true false test to see if the captcha has been solved
    def _captcha_solver(self):
        if self.test(self.driver, self.captcha_test_xpath) is True:
            self._recaptcha_V2_solver()
            self._inject_response()
            time.sleep(2)
            return False
        else:
            return True
    
    # this function creates a while loop to keep trying to solve a captcha until the _captcha_solver returns a success
    # the while loop is necessary in cases when:
        # the captcha solving service returns an error
        # the website throws multiple captchas at the bot
    def _captcha_solver_loop(self):
        while self.result is False:
            try:
                self.result = self.captcha_solver()
            except:
                raise InjectionError('An error occured while trying to inject captcha solution into webpage.')

    # this function is the entry point
    def solve(self, driver, sitekey, apikey, captcha_test_xpath, callback_function):           
        self.driver = driver
        self.sitekey = sitekey
        self.apikey = apikey
        self.captcha_test_xpath = captcha_test_xpath
        self.callback_function = callback_function
        self.result = False
        self.captcha_test_xpath = captcha_test_xpath
        self._captcha_solver()
    
    # this function returns a boolean test if captcha is visible
    # user has to make the recaptcha test appear
    def test(self, driver, captcha_test_xpath):
        self.driver = driver
        self.captcha_test_xpath = captcha_test_xpath 
        self.captcha_test = self.driver.find_element_by_xpath(self.captcha_test_xpath).get_attribute('style')[12:19]
        if self.captcha_test == 'visible':
            return True
        else:
            return False