import importlib
import logging
import traceback

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

    Keyword arguments:

    - cache_dir -- Path to cache directory for scraped file artifacts (default: {})
    - config_path -- Path to location of config file
    - place_id -- Scraper ID made up of state and county (e.g. ga_dekalb)

    """

    def __init__(self, cache_dir, config_path, place_id):
        self.cache_dir = cache_dir
        self.config_path = config_path
        self.place_id = place_id

    def search(self, terms=[], headless=True):
        """
        For a given scraper, executes the search, acquisition
        and processing of case info.

        Keyword arguments:

        - terms - List of search terms
        - headless - Whether or not to run headless (default: True)

        Returns: List of dicts containing case metadata
        """
        SiteKls = self._get_site_class()
        url = self.site_meta['home_url']
        username, password = self._get_login_creds()
        args = [url]
        if username and password:
            args.extend([username, password])
        try:
            site = SiteKls(
                *args,
                self.cache_dir,
                headless=headless
            )
            if username and password:
                site.login()
            data = site.search(terms=terms, headless=headless)
            success_msg = "{} search ran successfully".format(self.place_id)
            logger.info(success_msg)
            return data
        except Exception as e:
            message = '{} search raised an error\n'.format(self.place_id)
            message += ''.join(traceback.format_tb(e.__traceback__))
            logger.error(message)

    def list_scrapers(self):
        """
        List available scrapers.

        Returns: List of scraper names and IDs.

        """
        #return [str(ScraperKls()) for ScraperKls in self.scrapers()]
        # TODO: List available scrapers using SiteMeta
        pass

    def _get_site_class(self):
        # Site types for one-off scrapers should live in
        # a module for state and county, e.g. ny_westchester.
        # This module name should match the site_type in sites_meta.csv
        if self.place_id == self.site_type:
            target_module = 'court_scraper.scrapers.{}'.format(place_id)
        else:
            target_module = 'court_scraper.platforms.{}'.format(site_type)
        mod = importlib.import_module(target_module)
        kls_name = self.site_type.title().replace('_','').lower()
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
