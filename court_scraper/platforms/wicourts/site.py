from datetime import date

import requests

from court_scraper.base.selenium_site import SeleniumSite
from court_scraper.case_info import CaseInfo
from court_scraper.utils import dates_for_range
#from .pages.case_detail import CaseDetails
from .pages.search import SearchPage

from .search_api import SearchApi


class WicourtsSite(SeleniumSite):

    current_day = date.today().strftime("%Y-%m-%d")

    def __init__(self, place_id, captcha_api_key=None):
        self.captcha_api_key = captcha_api_key
        self.place_id = place_id
        self.url = "https://wcca.wicourts.gov/advanced.html"

    def search_by_date(self,
            start_date=None,
            end_date=None,
            case_details=False,
            download_dir=None,
            extra_params={}
        ):
        #if not start_date:
        #    start_date, end_date = self.current_day, self.current_day
        date_format = "%m-%d-%Y"
        dates = dates_for_range(start_date, end_date, output_format=date_format)
        results = []
        for date_str in dates:
            api = SearchApi(self.place_id[3:]) # Clip the state prefix from place_id
            if case_details:
                #TODO: invoke self.search
                pass
            else:
                cases = api.search_by_date(date_str, date_str, extra_params=extra_params)
            results.append(cases)
        return results

    def search(self,
           download_dir,
           case_numbers=[],
           start_date=None,
           end_date=None,
           case_types=[],
           case_details=True,
           headless=True
        ):
        # TODO: If one or more case_numbers provided, execute a selenium search
        # for case numbers in county)
        results = []
        if case_numbers:
            pass
        # Otherwise, perform a date_based search for county
        try:
            self.download_dir = download_dir
            self.driver = self._init_chrome_driver(headless=headless)
            search_page = SearchPage(self.driver, self.captcha_api_key)
            data = search_page.search_by_date(self.place_id[3:], start_date, end_date)
            results.extend(data)
        finally:
            try:
                self.driver.quit()
            except AttributeError:
                pass
        return results

    def _get_case_info_mapped_class(self):
        mapping = {
            'case_num': 'number',
            'file_date': 'filing_date',
        }
        CaseInfo._map = mapping
        return CaseInfo
