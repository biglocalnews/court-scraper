import importlib
import os
from pathlib import Path

from court_scraper.sites_meta import SitesMeta


class Site:

    def __new__(cls, *args, **kwargs):
        place_id = args[0]
        meta = cls.get_site_meta(cls, place_id)
        site_type = meta['site_type']
        site_class = cls.get_site_class(cls, place_id, site_type)
        if site_type == 'odyssey':
            url = meta['home_url']
            download_dir = cls.get_download_dir(cls, place_id)
            final_args = [url, download_dir]
        else:
            final_args = args
        return site_class(*final_args, **kwargs)

    def get_download_dir(cls, place_id):
        try:
            court_scraper_dir = os.environ['COURT_SCRAPER_DIR']
        except KeyError:
            court_scraper_dir = '/tmp'
        return str(Path(court_scraper_dir, f'cache/{place_id}'))

    def get_site_meta(cls, place_id):
        sm = SitesMeta()
        state = place_id[0:2]
        county = place_id[3:].replace('_', ' ').strip()
        key = (state, county)
        site_info = sm.data[key]
        cls._site_meta = site_info
        return cls._site_meta

    def get_site_class(cls, place_id, site_type):
        """Look up Site class by place ID and site type.

        Site types for one-off scrapers should live in the 'scrapers'
        namespace in a module named by state and county, e.g. ny_westchester.

        Platform site classes should live in platforms namespace (e.g. odyssey).

        In both cases, sites_meta.csv should specify the module name
        in the site_type field as a snake_case value (ny_westchester).

        """
        if place_id == site_type:
            parent_mod = 'scrapers'
        else:
            parent_mod = 'platforms'
        target_module = 'court_scraper.{}.{}'.format(parent_mod, site_type)
        mod = importlib.import_module(target_module)
        return getattr(mod, 'Site')
