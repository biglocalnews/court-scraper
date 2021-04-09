import importlib
import logging
import traceback
from pathlib import Path

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader


logger = logging.getLogger(__name__)

from .sites_meta import SitesMeta

class ScraperError(Exception): pass


class Runner:
    """
    Facade class to simplify invocation and usage of scrapers.

    Arguments:

    - cache_dir -- Path to cache directory for scraped file artifacts (default: {})
    - config_path -- Path to location of config file
    - place_id -- Scraper ID made up of state and county (e.g. ga_dekalb)

    """

    def __init__(self, cache_dir, config_path, place_id):
        self.cache_dir = cache_dir
        self.config_path = config_path
        self.place_id = place_id

    def search(self, search_terms=[], headless=True):
        """
        For a given scraper, executes the search, acquisition
        and processing of case info.

        Keyword arguments:

        - search_terms - List of search terms
        - headless - Whether or not to run headless (default: True)

        Returns: List of dicts containing case metadata
        """
        SiteKls = self._get_site_class()
        url = self.site_meta['home_url']
        username, password = self._get_login_creds()
        pos_args = [url]
        site = SiteKls(
            *pos_args,
            self.cache_dir,
            headless=headless
        )
        if username and password:
            site.login(username, password)
        logger.info(
            "Executing search for {}".format(self.place_id)
        )
        data = site.search(search_terms=search_terms)
        return data


    def cache_detail_pages(self, search_results):
        """
        Caches HTML source, if available, for case detail pages

        Arguments:
        - search_results (list of CaseInfo instances)

        Return value: None
        """
        for case in search_results:
            try:
                page_source = case.page_source
            except AttributeError:
                continue
            outdir = Path(self.cache_dir)\
                .joinpath('cache')\
                .joinpath(self.place_id)
            outdir.mkdir(parents=True, exist_ok=True)
            outfile = str(
                outdir.joinpath('{}.html'.format(case.number))
            )
            logger.info('Caching file: {}'.format(outfile))
            with open(outfile, 'w') as fh:
                fh.write(page_source)

    def parse_html_pages(self, html_pages):
        """ 
        Function should call a platform and place-specific parser;
        Base parser provides functionality for opening html and saving json;

        """
        pass

    def _get_site_class(self):
        # Site types for one-off scrapers should live in the scrapers
        # namespace in a module named by state and county, e.g. ny_westchester.
        # Platform site classes should live in platforms namespace
        # in a snake_case module (e.g. odyssey_site).
        # In both cases, sites_meta.csv should specify the module name
        # in the site_type field as a snake_case value (ny_westchester, odyssey_site).
        if self.place_id == self.site_type:
            parent_mod = 'scrapers'
        else:
            parent_mod = 'platforms'
        target_module = 'court_scraper.{}.{}'.format(parent_mod, self.site_type)
        mod = importlib.import_module(target_module)
        kls_name = self.site_type.title().replace('_','')
        return getattr(mod, kls_name)

    @property
    def site_type(self):
        return self.site_meta['site_type']

    @property
    def site_meta(self):
        try:
            return self._site_meta
        except AttributeError:
            sm = SitesMeta()
            key = tuple(self.place_id.split('_'))
            site_info = sm.data[key]
            self._site_meta = site_info
            return self._site_meta

    def _get_login_creds(self):
        with open(self.config_path,'r') as fh:
            username = None
            password = None
            configs = yaml.load(fh, Loader=Loader)
            try:
                config = configs[self.place_id]
                username = config['username']
                password = config['password']
            except KeyError:
                    pass
            return (username, password)


