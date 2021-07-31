import os
import shutil
from pathlib import Path

from my_fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class SeleniumSite:

    def _init_chrome_driver(self, headless=True):
        chrome_options = self._build_chrome_options(headless=headless)
        executable_path = shutil.which('chromedriver')
        driver = webdriver.Chrome(options=chrome_options, executable_path=executable_path)
        return driver

    def _build_chrome_options(self, headless=True, random_user=False):
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--verbose')
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False
        })
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
        if headless:
            chrome_options.add_argument("--headless")
        if random_user:
            ua = UserAgent(family='chrome')
            randomua = ua.random()
            chrome_options.add_argument(f'user-agent={randomua}')
        return chrome_options

    def get_download_dir(self):
        try:
            court_scraper_dir = os.environ['COURT_SCRAPER_DIR']
        except KeyError:
            court_scraper_dir = '/tmp/court-scraper'
        return str(Path(court_scraper_dir, f'cache/{self.place_id}'))
