import time

from anticaptchaofficial.recaptchav2proxyless import *

from .recaptcha import Recaptcha


class InvisibleRecaptchaV2(Recaptcha):


    def solve(self, driver, sitekey, apikey, captcha_test_xpath, callback_function):
        """Main entry point"""
        self.driver = driver
        self.sitekey = sitekey
        self.apikey = apikey
        self.captcha_test_xpath = captcha_test_xpath
        self.callback_function = callback_function
        self.result = False
        self.captcha_test_xpath = captcha_test_xpath
        self._captcha_solver()

    def _inject_response(self):
        """Get captcha response and inject via callback function"""
        self.driver.execute_script(f'{self.callback_function}("{self.g_response}")')

    def _captcha_solver(self):
        """Create a true false test to see if the captcha has been solved"""
        if self.test(self.driver, self.captcha_test_xpath) is True:
            self._recaptcha_V2_solver()
            self._inject_response()
            time.sleep(2)
            return False
        else:
            return True

    def _captcha_solver_loop(self):
        """Creates a while loop to keep trying to solve a captcha until the _captcha_solver returns a success

        Necessary in cases when:
         - captcha solving service returns an error
         - website throws multiple captchas at the bot
        """
        while self.result is False:
            try:
                self.result = self.captcha_solver()
            except:
                raise InjectionError('An error occured while trying to inject captcha solution into webpage.')

    def test(self, driver, captcha_test_xpath):
        """Test if captcha is visible

        User has to make the recaptcha test appear
        """
        self.driver = driver
        self.captcha_test_xpath = captcha_test_xpath
        self.captcha_test = self.driver.find_element_by_xpath(self.captcha_test_xpath).get_attribute('style')[12:19]
        if self.captcha_test == 'visible':
            return True
        else:
            return False
