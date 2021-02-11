from anticaptchaofficial.recaptchav2proxyless import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .recaptcha import Recaptcha

class RecaptchaV2(Recaptcha):
    
    def _inject_response(self):
        self.driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML = "{self.g_response}"')
    def _submit(self):
        if self.script_submit != None:
            self.driver.execute_script(self.script_submit)
        elif self.xpath_submit != None:
            self.driver.find_element_by_xpath(self.xpath_submit).click()
        else:
            raise SubmitException('no way to submit provided')
        
    def _solve(self):
        try:
            self._recaptcha_V2_solver()
        except:
            raise AntiCaptchaError('AntiCaptcha returned an error')
        try:
            self._inject_response()
        except:
            raise InjectionError('cannot find g-recaptcha-response ID')
        try:
            self._submit()
        except:
            raise SubmitError('provided submit option is not working')
    
    # this function is the entry point
    def solve(self, driver, sitekey, apikey, script_submit=None, xpath_submit=None):           
        self.driver = driver
        self.sitekey = sitekey
        self.apikey = apikey
        self.script_submit = script_submit
        self.xpath_submit = xpath_submit
        self._solve()