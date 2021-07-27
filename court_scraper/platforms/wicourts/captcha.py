from selenium.webdriver.common.by import By

from court_scraper.captcha.invisible_recaptcha_v2 import InvisibleRecaptchaV2


class CaptchaVariables:
    SITEKEY = '6LeTUtAUAAAAALyw0QQWmOALx9f2eDS2Y23m6eVp'
    APIKEY = ''
    CALLBACK_FUNCTION = '___grecaptcha_cfg.clients[0].O.O.callback'
    CAPTCHA_TYPE = 'recaptcha_V2'
    CAPTCHA = (By.XPATH, '/html/body/div[2]')


class CaptchaHelpers():

    captcha = InvisibleRecaptchaV2()
    variables = CaptchaVariables()

    def test_captcha(self):
        return self.captcha.test(self.driver, self.variables.CAPTCHA[1])

    def solve_captcha(self):
        self.captcha.solve(
            self.driver, self.variables.SITEKEY, self.variables.APIKEY,
            self.variables.CAPTCHA[1],  self.variables.CALLBACK_FUNCTION
        )

    def save_cookies(self):
        pickle.dump(self.driver.get_cookies(), open(f'{cache_dir}/cookies.pkl', 'wb'))

    def load_cookies(self):
        cookies = pickle.load(open(f'{cache_dir}/cookies.pkl', 'rb'))
        for cookie in cookies:
                self.driver.add_cookie(cookie)


