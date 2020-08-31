import shutil

from my_fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class SeleniumSite:


    def _init_chrome_driver(self, headless=True):
        chrome_options = self._build_chrome_options(headless=headless)
        executable_path = shutil.which('chromedriver')
        driver = webdriver.Chrome(options=chrome_options, executable_path=executable_path)
        return driver

    def _build_chrome_options(self, headless=True):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--verbose')
        chrome_options.add_experimental_option("prefs", {
                "download.default_directory": self.download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing_for_trusted_sources_enabled": False,
                "safebrowsing.enabled": False
        })
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
        ua = UserAgent(family='chrome')
        randomua = ua.random()
        chrome_options.add_argument(f'user-agent={randomua}')
        return chrome_options


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def fill_form_field(self, locator_name, value):
        element = self._get_element_by_locator(locator_name)
        element.send_keys(value)

    def click(self, locator_name):
        element = self._get_element_by_locator(locator_name)
        element.click()

    def _get_element_by_locator(self, locator_name):
        locator = getattr(self.locators, locator_name)
        return self.driver.find_element(*locator)
