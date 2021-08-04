from datetime import date
from typing import List

from court_scraper.case_info import CaseInfo
from .search_results_wrapper import SearchResultsWrapper
from .pages.case_number_lookup import CaseNumberLookup
from .pages.daily_filings import DailyFilings
from .pages.search import Search


# These counties are supported by
# DailyFilings by County search,
DAILY_FILING_COUNTIES = [
    'ok_adair',
    'ok_canadian',
    'ok_cleveland',
    'ok_comanche',
    'ok_ellis',
    'ok_garfield',
    'ok_logan',
    'ok_oklahoma',
    'ok_payne',
    'ok_pushmataha',
    'ok_roger_mills',
    'ok_rogers',
    'ok_tulsa',
]


class Site:

    current_day = date.today().strftime("%Y-%m-%d")

    def __init__(self, place_id):
        self.place_id = place_id

    def __repr__(self):
        return f'Oscn ({self.place_id})'

    def search(self, case_numbers=[], **kwargs) -> List[CaseInfo]:
        """Search one or more case IDs in a given county.

        Args:
            case_numbers (list<case numbers>): One or more case numbers

        Returns:

            List of :py:class:`CaseInfo <court_scraper.case_info.CaseInfo>` instances

        """
        # NOTE: place_id will be a county typically, but we could at some
        # point support a state-wide search
        lookup = CaseNumberLookup(self.place_id)
        return lookup.search(case_numbers=case_numbers)

    def search_by_date(self, start_date=None, end_date=None, case_details=False) -> SearchResultsWrapper:
        """Search for cases by date range

        Searches current day by default. Optionally scrapes case detail pages.

        For searches spanning a wide range of dates (with potentially lots of
        of results), calling code should generate date ranges and invoke this method day by day.
        This will enable the caller to cache results and avoid losing data from
        if an exception occurs during a long-running scrape.

        Args:
            start_date (str): Date as YYYY-MM-DD. Default: current day
            end_date (str): Date as YYYY-MM-DD. Default: current day
            case_details (boolean): Scrape data from case detail pages. Default: False

        Returns:
            A dict-like :py:class:`SearchResultsWrapper
            <court_scraper.platforms.oscn.search_results_wrapper.SearchResultsWrapper>`
            instance with date-based keys (YYYY-MM-DD) and dict values
            containing `html` and `cases` as keys. The latter contains a list of
            :py:class:`CaseInfo <court_scraper.case_info.CaseInfo>` instances.

        """
        # Use Daily Filings where available, and fall back to generic
        # Search (latter supports all counties but truncates results at 500)
        if self.place_id in DAILY_FILING_COUNTIES:
            search_obj = DailyFilings(self.place_id)
        else:
            search_obj = Search(self.place_id)
        if not start_date:
            start_date, end_date = self.current_day, self.current_day
        results = search_obj.search(start_date, end_date, case_details=case_details)
        return results
