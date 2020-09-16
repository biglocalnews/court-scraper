from selenium.webdriver.common.by import By

class WisconsinURLs:
    
    CASE_DETAILS = 'https://wcca.wicourts.gov/caseDetail.html'
    SEARCH_PAGE = 'https://wcca.wicourts.gov/advanced.html'
    
class WisconsinVariables:
    
    SITEKEY = '6LeTUtAUAAAAALyw0QQWmOALx9f2eDS2Y23m6eVp'
    APIKEY = ''
    CALLBACK_FUNCTION = '___grecaptcha_cfg.clients[0].O.O.callback'
    CAPTCHA_TYPE = 'recaptcha_V2'

class CaptchaLocators:

    CAPTCHA = (By.XPATH, '/html/body/div[2]')