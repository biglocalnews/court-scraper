from selenium.webdriver.common.by import By

class CaptchaVariables:
    
    SITEKEY = '6LeTUtAUAAAAALyw0QQWmOALx9f2eDS2Y23m6eVp'
    APIKEY = ''
    CALLBACK_FUNCTION = '___grecaptcha_cfg.clients[0].O.O.callback'
    CAPTCHA_TYPE = 'recaptcha_V2'
    CAPTCHA = (By.XPATH, '/html/body/div[2]')