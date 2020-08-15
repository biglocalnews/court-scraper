import shutil

from my_fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .pages.case_detail import CaseDetailPage
from .pages.login import LoginPage
from .pages.portal import PortalPage
from .pages.search import SearchPage
from .pages.search_results import SearchResultsPage


class OdysseySite:

    def __init__(self, url, username, password, download_dir, timeout=60):
        self.site_url = url
        self.username = username
        self.password = password
        self.download_dir = download_dir
        self.timeout = timeout

    def login(self, headless=True):
        self.driver = self._init_chrome_driver(headless=headless)
        login_page = LoginPage(
            self.driver,
            self.site_url,
            self.username,
            self.password
        )
        login_page.go_to()
        login_page.login()

    def search(self, search_terms=[], get_detail_page_html=False, headless=True):
        portal_page = PortalPage(self.driver)
        portal_page.go_to_smart_search()
        results = []
        try:
            for term in search_terms:
                search_page = SearchPage(self.driver)
                search_page.search_box = term
                search_page.submit_search(self.timeout)
                results_page = SearchResultsPage(self.driver)
                if results_page.results_found():
                    for case_row in results_page.results:
                        row_data = case_row.metadata
                        if get_detail_page_html:
                            case_row.detail_page_link.click()
                            detail_page = CaseDetailPage(self.driver)
                            row_data['page_source'] = detail_page.page_source
                            results_page.back_to_search_results()
                        results.append(row_data)
            return results
        finally:
            self.driver.quit()

    def _init_chrome_driver(self, headless=True):
        chrome_options = self._build_chrome_options(headless=headless)
        executable_path = shutil.which('chromedriver')
        driver = webdriver.Chrome(options=chrome_options, executable_path=executable_path)
        return driver

    def _build_chrome_options(self, headless=True):
        # this code alters the browser to download the pdfs
        # it was taken from https://medium.com/@moungpeter/how-to-automate-downloading-files-using-python-selenium-and-headless-chrome-9014f0cdd196
        def enable_download_headless(browser, download_dir):
            browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
            params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
            browser.execute("send_command", params)
        # Options were slightly modified by commenting out things I didn't want
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


