import requests
from lxml import html
from fake_useragent import UserAgent
from io import StringIO, BytesIO

from base._last_date import LastDate
from base.requests_base import RequestsPage
from .ok_urls import OklahomaURLs


class SearchPage(RequestsPage):
    
    url = OklahomaURLs.search_page
    parser = etree.HTMLParser()
    
    def __init__(self):
        self.lastdate = LastDate()
        
    def _get_last_workday(self, subtract_days = 1):
        self.url_date = self.lastdate.date_to_search(self.year, subtract_days = subtract_days).strftime("%m/%d/%y")
        self.payload = {
            'report' : 'DailyFilings',
            'errorcheck' : 'true',
            'database' : '',
            'db' : self.county,
            'StartDate' : self.url_date
                       }
    
    def _subtract_another_day(self, subtract_days = 1):
        
        self.subtract_days = self.subtract_days + subtract_days
        
    def _parse_case_table(self):
        self.tree = etree.parse(StringIO(self.output.text), self.parser)
        self.case_rows = self.tree.xpath(f'//*[contains(text(), "{self.case_prefix}-")]')
        self.case_number = self.case_rows[len(self.case_rows)-1].text
        return self.case_number
        
        
    def _search_previous_day_until_success(self):
        result = None
        while result is None:
            try:
                print('subtracting another day')
                self._subtract_another_day()
                print('getting next workday')
                self._get_last_workday(subtract_days = self.subtract_days)
                print('calling new html search')
                self.output = self.get_html(self.url, payload = self.payload)
                print(f'attempting to parse case table for {self.url_date}')
                result = self._parse_case_table()
            except IndexError:
                pass  
        return result
        

        
    def most_recent_case(self, county, year, case_prefix):
        self.county = county
        self.year = year
        self.case_prefix = case_prefix
        self._get_last_workday()
        self.output = self.get_html(self.url, payload = self.payload)      
        try:
            return self._parse_case_table()
        except IndexError:
            return self._search_previous_day_until_success()