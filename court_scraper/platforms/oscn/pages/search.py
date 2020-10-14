import requests
from lxml import html
from fake_useragent import UserAgent
from io import StringIO, BytesIO

from court_scraper.base.last_date import LastDate
from court_scraper.base.requests_base_page import RequestsBasePage
from court_scraper.base.search_page_mixin import SearchPageMixIn
from .url import OklahomaURLs

class Search(RequestsBasePage, SearchPageMixIn):
    
    url = OklahomaURLs.search_page
        
    def _get_last_workday(self, subtract_days = 1):
        #self.url_date = self.lastdate.date_to_search(self.year, subtract_days = subtract_days).strftime("%m/%d/%y")
        super()._get_last_workday()
        self.payload = {
            'report' : 'DailyFilings',
            'errorcheck' : 'true',
            'database' : '',
            'db' : self.county,
            'StartDate' : self.url_date
                       }