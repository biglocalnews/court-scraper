import requests
from court_scraper.utils import dates_for_range
from .base_search import BaseSearch
from .daily_filings_results import DailyFilingsResultsPage
from ..search_results_wrapper import SearchResultsWrapper


class DailyFilings(BaseSearch):
    """Search daily filings by county for limited number of larger counties.

    Supports searches by date only.

    Args:
        - place_id (str): Standard place id (e.g. ok_tulsa or ok_roger_mills)

    """

    def __init__(self, place_id):
        self.url = 'https://www.oscn.net/applications/oscn/report.asp'
        self.place_id = place_id

    def search(self, start_date, end_date, case_details=False):
        date_format = "%m-%d-%y"
        dates = dates_for_range(start_date, end_date, output_format=date_format)
        search_results = SearchResultsWrapper()
        for date_str in dates:
            # Convert date_str to standard YYYY-MM-DD for upstream usage
            date_key = self._standardize_date(date_str, date_format, "%Y-%m-%d")
            html, basic_case_data = self._run_search_for_day(date_str)
            # Skip if there were no results for date
            if not basic_case_data:
                continue
            search_results.add_html(date_key, html)
            if case_details:
                self._scrape_case_details(date_key, search_results, basic_case_data)
            else:
                search_results.add_case_data(date_key, basic_case_data)
        return search_results

    def _run_search_for_day(self, day):
        payload = {
            'report': 'DailyFilings',
            'errorcheck': 'true',
            'database': '',
            'db': self._place,
            'StartDate': day
        }
        response = requests.get(self.url, params=payload)
        html = response.text
        page = DailyFilingsResultsPage(self.place_id, response.text)
        return html, page.results
