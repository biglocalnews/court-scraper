import importlib
import logging
from pathlib import Path

import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


from court_scraper.sites_meta import SitesMeta


logger = logging.getLogger(__name__)


class BaseRunner:
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

    def search(self, case_numbers=[], headless=True):
        """Should invoke Site.search

        Override this on base runner classes.
        """
        raise NotImplementedError

    def cache_detail_pages(self, search_results):
        """
        Caches HTML source, if available, for case detail pages

        Arguments:
        - search_results (list of CaseInfo instances)

        Return value: None
        """
        for case in search_results:
            # Gross. We should standardize to page_source or html
            try:
                page_source = case.page_source
            except AttributeError:
                page_source = case.html
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
        # Platform site classes should live in platforms namespace (e.g. odyssey).
        # In both cases, sites_meta.csv should specify the module name
        # in the site_type field as a snake_case value (ny_westchester).
        if self.place_id == self.site_type:
            parent_mod = 'scrapers'
        else:
            parent_mod = 'platforms'
        target_module = 'court_scraper.{}.{}'.format(parent_mod, self.site_type)
        mod = importlib.import_module(target_module)
        return getattr(mod, 'Site')

    @property
    def site_type(self):
        return self.site_meta['site_type']

    @property
    def site_meta(self):
        try:
            return self._site_meta
        except AttributeError:
            sm = SitesMeta()
            state = self.place_id[0:2]
            county = self.place_id[3:].replace('_', ' ').strip()
            key = (state, county)
            site_info = sm.data[key]
            self._site_meta = site_info
            return self._site_meta

    def _get_login_creds(self):
        with open(self.config_path, 'r') as fh:
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
