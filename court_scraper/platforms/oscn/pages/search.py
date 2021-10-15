import logging
import requests
from fake_useragent import UserAgent

from court_scraper.utils import dates_for_range
from .base_search import BaseSearch
from .search_results import SearchResultsPage


logger = logging.getLogger(__name__)
ua = UserAgent()

class Search(BaseSearch):



    """General search page for all OK counties.

    Supports searches by date, case type and a variety of other
    parameters. Large searches are truncated, so searches using
    this class should be targeted narrowly (e.g. a single day
    for smaller counties). For larger counties such as Tulsa,
    use DailyFilings search class.

    Args:
        place_id (str): Standard place id (e.g. ok_alfalfa)

    """

    def __init__(self, place_id):
        self.url = 'https://www.oscn.net/dockets/Results.aspx'
        self.place_id = place_id

    def search(self, start_date, end_date, extra_params={}, case_details=False):
        date_format = "%m/%d/%Y"
        dates = dates_for_range(start_date, end_date, output_format=date_format)
        search_results = []
        for date_str in dates:
            # Convert date_str to standard YYYY-MM-DD for upstream usage
            date_key = self._standardize_date(date_str, date_format, "%Y-%m-%d")
            # Always limit query to a single filing date, to minimize
            # chances of truncate results
            search_params = {
                'FiledDateL': date_str,  # start filing date - MM/DD/YYYY
                'FiledDateH': date_str,  # end filing date - MM/DD/YYYY
            }
            # Merge any additional query parameters
            search_params.update(extra_params)
            html, basic_case_data = self._run_search(search_params)
            # Skip if there were no results for date
            if not basic_case_data:
                continue
            # Warn if results were truncated
            if 'results are limited to 500' in html:
                msg = (
                    "WARNING: Results were truncated for your search."
                    " Try using a more targeted query, e.g. with a case type, "
                    " to avoid losing records."
                )
                logger.warning(msg)
            if case_details:
                results = self._scrape_case_details(date_key, basic_case_data)
                search_results.extend(results)
            else:
                # Add the filing date to CaseInfo instances if it's only a metadata search
                # since it's not listed on results page
                for case in basic_case_data:
                    case.update({'filing_date': date_key})
                    search_results.append(case)
        return search_results

    def _run_search(self, search_params):
        params = self._default_params
        # Always add place to search
        params['db'] = self._place
        headers = {'User-Agent': ua.random}
        # Add any extra params (typically will include filing date)
        params.update(search_params)
        response = requests.get(self.url, params=params, headers=headers)
        html = response.text
        page = SearchResultsPage(self.place_id, html)
        return html, page.results

    @property
    def _default_params(self):
        return {
            'db': '',  # county court name (lowercase, no spaces , e.g. rogermills)
            'number': '',
            'lname': '',
            'fname': '',
            'mname': '',
            'DoBMin': '',
            'DoBMax': '',
            'partytype': '',
            'apct': '',
            'dcct': '',
            'FiledDateL': '',  # start filing date - MM/DD/YYYY
            'FiledDateH': '',  # end filing date - MM/DD/YYYY
            'ClosedDateL': '',
            'ClosedDateH': '',
            'iLC': '',
            'iLCType': '',
            'iYear': '',
            'iNumber': '',
            'citation': '',
        }
