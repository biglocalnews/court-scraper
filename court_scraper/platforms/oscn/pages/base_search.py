import datetime

from .case_number_lookup import CaseNumberLookup


class BaseSearch:
    """Base class with shared code for DailyFilings and Search
    """

    def _scrape_case_details(self, date_key, search_results, basic_case_data):
        """Loop through CaseInfo classes from upstream search results,
        scrape case details, and merge data for CaseInfo from both sources
        """
        for basic_case in basic_case_data:
            lookup = CaseNumberLookup(self.place_id)
            # Get single CaseInfo class from CaseNumberLookup
            case_info = lookup.search([basic_case.number])[0]
            # Merge basic CaseInfo (from search results page)
            # with CaseInfo (from case detail page)
            basic_case.merge(case_info)
            # ...and add to search results, which expects a list
            search_results.add_case_data(date_key, [basic_case])

    def _standardize_date(self, date_str, from_format, to_format):
        return datetime.datetime.strptime(date_str, from_format).strftime(to_format)

    @property
    def _place(self):
        county_bits = self.place_id.replace('_', ' ').split(' ')[1:]
        return " ".join(county_bits).title()
