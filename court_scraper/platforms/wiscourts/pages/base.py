from my_fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from court_scraper.base.selenium_base import SeleniumPage
from court_scraper.base.captcha_solver import CaptchaSolvers
from .config import *

class WisconsinBasePage(SeleniumPage):
    
    captcha = CaptchaSolvers()
    locators = CaptchaLocators()
    variables = WisconsinVariables()
    
    def __init__(self, driver, url):
        super().__init__(driver)
        self.site_url = url
    
    def go_to(self):
        self.driver.get(self.site_url)
        time.sleep(1)
    
    def test_captcha(self):
        return self.captcha.test(self.driver, self.locators.CAPTCHA[1])
        
        
    def solve_captcha(self):
        self.captcha.solve(
            self.driver, self.variables.CAPTCHA_TYPE, 
            self.variables.SITEKEY, self.variables.APIKEY, 
            self.locators.CAPTCHA[1],  self.variables.CALLBACK_FUNCTION
        )
         
    def save_cookies(self):
        pickle.dump(self.driver.get_cookies(), open(f'{cache_dir}/cookies.pkl', 'wb'))
    
    def load_cookies(self):
        cookies = pickle.load(open(f'{cache_dir}/cookies.pkl', 'rb'))
        for cookie in cookies:
                self.driver.add_cookie(cookie)