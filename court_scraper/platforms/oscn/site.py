from datetime import date
from .pages.case_number_lookup import CaseNumberLookup
from .pages.daily_filings import DailyFilings



class Site:

    current_day = date.today().strftime("%Y-%m-%d")

    def __init__(self, place_id):
        self.place_id = place_id

    def search(self, search_terms=[], **kwargs):
        """Search one or more case IDs in a given county.

        Args:
            search_terms (list<case numbers>): One or more case numbers

        Returns:

            List of CaseInfo classes

        """
        results = []
        # NOTE: place_id will be a county typically, but we could at some
        # point support a state-wide search
        lookup = CaseNumberLookup(self.place_id)
        return lookup.search(case_numbers=search_terms)

    def search_by_date(self, start_date=None, end_date=None, case_details=False):
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
            SearchResults object with date-based keys (YYYY-MM-DD) and a dict value
            containing HTML and list of CaseInfo objects: {'html': '<etc>', 'cases': [CaseInfo, etc.]}

        """
        df = DailyFilings(self.place_id)
        if not start_date:
            start_date, end_date = self.current_day, self.current_day
        results = df.search(start_date, end_date, case_details=case_details)
        return results
