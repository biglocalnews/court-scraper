# Scraping
# Logging
import logging

from court_scraper.base.runner import BaseRunner

from .site import Site

logger = logging.getLogger(__name__)


class Runner(BaseRunner):
    """
    Runs the Iowa court scraper via a CLI

    Arguments:

    - cache_dir -- Path to cache directory for scraped file artifacts (default: {})
    - config_path -- Path to location of config file
    - place_id -- Scraper ID made up of state and county (e.g. ga_dekalb)
    """

    def search(self, case_numbers=[], **kwargs):
        """
        Search the provided case numbers in the Iowa courts site.

        Keyword arguments:

        - case_numbers - List of case numbers

        Returns: List of dicts containing case metadata
        """
        site = Site(place_id=self.place_id)
        logger.info(f"Executing {self.place_id} search")
        return site.search(case_numbers=case_numbers, **kwargs)
