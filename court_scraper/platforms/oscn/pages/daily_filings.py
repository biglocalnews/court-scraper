import datetime
import requests

from court_scraper.utils import dates_for_range
from .case_number_lookup import CaseNumberLookup

from .daily_filings_results import DailyFilingsResultsPage
from ..search_results_wrapper import SearchResultsWrapper


class DailyFilings:

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
                # Loop through CaseInfo classes from DailyFiling search
                for basic_case in basic_case_data:
                    lookup = CaseNumberLookup(self.place_id)
                    # Get single CaseInfo class from CaseNumberLookup
                    case_info = lookup.search([basic_case.number])[0]
                    # Merge basic CaseInfo (from search results page)
                    # with CaseInfo (from case detail page)
                    basic_case.merge(case_info)
                    # ...and add to search results, which expects a list
                    search_results.add_case_data(date_key, [basic_case])
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

    @property
    def _place(self):
        county_bits = self.place_id.replace('_', ' ').split(' ')[1:]
        return " ".join(county_bits).title()

    def _standardize_date(self, date_str, from_format, to_format):
        return datetime.datetime.strptime(date_str, from_format).strftime(to_format)
