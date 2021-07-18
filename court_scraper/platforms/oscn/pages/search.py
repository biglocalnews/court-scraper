import datetime
import requests

from court_scraper.case_info import CaseInfo
from court_scraper.utils import dates_for_range
from .case_number_lookup import CaseNumberLookup

from .search_results import SearchResultsPage
from ..search_results_wrapper import SearchResultsWrapper



class Search:
    """General search page for all OK counties.

    Supports searches by date, case type and a variety of other
    parameters. Large searches are truncated, so searches using
    this class should be targeted narrowly (e.g. a single day
    for smaller counties).

    Args:
        - place_id (str): Standard place id (e.g. ok_alfalfa or ok_roger_mills)

    Returns:

        SearchResultsWrapper class containing html of search results page and
        CaseInfo instances.

    """

    def __init__(self, place_id):
        self.url = 'https://www.oscn.net/dockets/Results.aspx'
        self.place_id = place_id

    def search(self, start_date, end_date, extra_params={}, case_details=False):
        date_format = "%m/%d/%Y"
        dates = dates_for_range(start_date, end_date, output_format=date_format)
        search_results = SearchResultsWrapper()
        for date_str in dates:
            # Convert date_str to standard YYYY-MM-DD for upstream usage
            date_key = self._standardize_date(date_str, date_format, "%Y-%m-%d")
            # Always limit query to a single filing date, to minimize
            # chances of truncate results
            search_params = {
                'FiledDateL': date_str, # start filing date - MM/DD/YYYY
                'FiledDateH': date_str, # end filing date - MM/DD/YYYY
            }
            # Merge any additional query parameters
            search_params.update(extra_params)
            html, basic_case_data = self._run_search(search_params)
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

    def _run_search(self, search_params):
        params = self._default_params
        # Always add place to search
        params['db'] = self._place
        # Add any extra params (typically will include filing date)
        params.update(search_params)
        response = requests.get(self.url, params=params)
        html = response.text
        page = SearchResultsPage(self.place_id, response.text)
        return html, page.results

    def _standardize_date(self, date_str, from_format, to_format):
        return datetime.datetime.strptime(date_str, from_format).strftime(to_format)

    @property
    def _place(self):
        county_bits = self.place_id.replace('_', ' ').split(' ')[1:]
        return " ".join(county_bits).title()

    @property
    def _default_params(self):
        return {
            'db': '', # county court name (lowercase, no spaces , e.g. rogermills)
            'number': '',
            'lname': '',
            'fname': '',
            'mname': '',
            'DoBMin': '',
            'DoBMax': '',
            'partytype': '',
            'apct': '',
            'dcct': '',
            'FiledDateL': '', #  start filing date - MM/DD/YYYY
            'FiledDateH': '', # end filing date - MM/DD/YYYY
            'ClosedDateL': '',
            'ClosedDateH': '',
            'iLC': '',
            'iLCType': '',
            'iYear': '',
            'iNumber': '',
            'citation': '',
        }
