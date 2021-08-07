import logging
from court_scraper.base.runner import BaseRunner
logger = logging.getLogger(__name__)


class Runner(BaseRunner):
    """
    Facade class to simplify invocation and usage of scrapers.

    Arguments:

    - cache_dir -- Path to cache directory for scraped file artifacts (default: {})
    - config_path -- Path to location of config file
    - place_id -- Scraper ID made up of state and county (e.g. ga_dekalb)

    """

    def search(self, case_numbers=[], headless=True):
        """
        For a given scraper, executes the search, acquisition
        and processing of case info.

        Args:

            case_numbers (list<str>):  List of case numbers to search
            headless (boolean): Whether or not to run headless (default: True)

        Returns:

            List of CaseInfo classes

        """
        SiteKls = self._get_site_class()
        url = self.site_meta['home_url']
        username, password = self._get_login_creds()
        pos_args = [self.place_id]
        site = SiteKls(
            *pos_args,
            url=url,
            download_dir=self.cache_dir,
            headless=headless
        )
        if username and password:
            site.login(username, password)
        logger.info(
            "Executing search for {}".format(self.place_id)
        )
        data = site.search(case_numbers=case_numbers)
        return data
