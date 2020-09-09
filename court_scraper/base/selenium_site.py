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
<<<<<<< Updated upstream:court_scraper/base/selenium_site.py
        return chrome_options


=======
        return chrome_options
>>>>>>> Stashed changes:court_scraper/base/selenium_base.py
