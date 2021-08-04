import selenium
from anticaptchaofficial.recaptchav2proxyless import recaptchaV2Proxyless
from court_scraper.configs import Configs


class CaptchaError(Exception):
    pass


def resolve_recaptcha_v2(method):
    """Decorate a Site class method with CAPTCHA handling via Anticaptcha service

    Assumes a Site class with a 'driver' attribute available on the instance
    """
    def wrapped(*args, **kwargs):
        driver = args[0].driver
        try:
            captcha_div = driver.find_element_by_css_selector('.g-recaptcha')
            site_key = captcha_div.get_attribute('data-sitekey')
            print(f're-captcha site-key: {site_key}')
            try:
                configs = Configs()
                anticaptcha_api_key = configs.captcha_service_api_key
            except KeyError:
                msg = f'CAPTCHA sites require Anticaptcha.com API key set in {configs.config_file_path}'
                raise CaptchaError(msg)
        except selenium.common.exceptions.NoSuchElementException:
            site_key = None
        if site_key:
            site_url = driver.current_url
            solver = recaptchaV2Proxyless()
            solver.set_verbose(1)
            solver.set_key(anticaptcha_api_key)
            solver.set_website_url(site_url)
            solver.set_website_key(site_key)
            g_response = solver.solve_and_return_solution()
            to_inject = f'document.querySelector(".g-recaptcha-response").innerHTML = "{g_response}";'
            driver.execute_script(to_inject)
        return method(*args, **kwargs)
    return wrapped
