import json
import logging
from pathlib import Path

from court_scraper.base.runner import BaseRunner
from court_scraper.configs import Configs
from .site import Site


logger = logging.getLogger(__name__)


class Runner(BaseRunner):
    """
    Facade class to simplify invocation and usage of scrapers.

    Args:

        cache_dir (str): Path to cache directory for scraped file artifacts (default: {})
        config_path (str): Path to location of config file
        place_id (str): Scraper ID made up of state and county (e.g. ga_dekalb)

    """

    def search(self, case_numbers=[], headless=True, **kwargs):
        """
        For a given scraper, executes the search, acquisition
        and processing of case info.

        Args:

            case_numbers (list<str>): List of case numbers to search
            headless (boolean): Whether or not to run headless (default: True)

        Returns:

            List of CaseInfo instances

        """
        # Look up the catcha API key as env variable, then fall back to config file
        configs = Configs()
        site = Site(self.place_id, captcha_api_key=configs.captcha_service_api_key)
        logger.info(
            "Executing search for {}".format(self.place_id)
        )
        data = site.search(case_numbers=case_numbers, headless=headless)
        return data

    def cache_detail_pages(self, search_results):
        """
        Caches JSON from case detail pages

        Args:

        - search_results (list of CaseInfo instances)

        Return value: None
        """
        for case in search_results:
            outdir = Path(self.cache_dir).joinpath('cache').joinpath(self.place_id)
            outdir.mkdir(parents=True, exist_ok=True)
            outfile = str(outdir.joinpath(f'{case.number}.json'))
            logger.info(f'Caching file: {outfile}')
            with open(outfile, 'w') as fh:
                json.dump(case.data, fh)
