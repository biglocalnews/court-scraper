from anticaptchaofficial.recaptchav2proxyless import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

# TODO: Support more captcha types.

class CaptchaSolvers:
    
    # this function returns boolean result based on visibility of captcha
    # the while loop in self.solve relies on this result
    def recaptcha_V2(self):
        if self.test(self.driver, self.captcha_test_xpath) is True:
            print('trying to solve captcha')
            self.recaptcha_V2_solver()
            time.sleep(2)
            return False
        else:
            print('captcha solved')
            return True
    
    # this function actually gets captcha response and injuects via callback function
    def recaptcha_V2_solver(self):
        self.solver = recaptchaV2Proxyless()
        self.solver.set_verbose(0)
        self.solver.set_key(self.apikey)
        self.solver.set_website_url(self.driver.current_url)
        self.solver.set_website_key(self.sitekey)
        print('calling captcha service')
        self.g_response = self.solver.solve_and_return_solution()
        print('injecting response')
        self.driver.execute_script(f'{self.callback_function}("{self.g_response}")')
    
    # this function will solve any type of captcha (we only support one type atm)
    # the while loop is necessary in cases when:
        # the captcha solving service returns an error
        # the
    def solve(self, driver, captcha_type, sitekey, apikey, captcha_test_xpath, callback_function):           
        self.captcha_type = captcha_type
        self.driver = driver
        self.sitekey = sitekey
        self.apikey = apikey
        self.captcha_test_xpath = captcha_test_xpath
        self.callback_function = callback_function
        result = False
        self.captcha_test_xpath = captcha_test_xpath
        if captcha_type == 'recaptcha_V2':
            print('loading recaptcha_V2 solver')
            while result is False:
                try:
                    result = self.recaptcha_V2()
                except:
                    raise Exception('While loop failed.')
        else:
            raise Exception('CaptchaNotSupported', 'only recaptcha_V2 is supported')
    
    # this function returns a boolean test if captcha is visible
    def test(self, driver, captcha_test_xpath):
        self.driver = driver
        self.captcha_test_xpath = captcha_test_xpath 
        self.captcha_test = self.driver.find_element_by_xpath(self.captcha_test_xpath).get_attribute('style')[12:19]
        if self.captcha_test == 'visible':
            return True
        else:
            return False