import importlib
from court_scraper.sites_meta import SitesMeta


class Site:

    def __new__(cls, *args, **kwargs):
        place_id = args[0]
        meta = cls.get_site_meta(cls, place_id)
        site_type = meta['site_type']
        site_class = cls.get_site_class(cls, place_id, site_type)
        # Odyssey is super non-standard
        if site_type == 'odyssey':
            # Set defaults for omitted kwargs
            if 'url' not in kwargs:
                kwargs['url'] = meta['home_url']
            if 'headless' not in kwargs:
                kwargs['headless'] = True
            final_args = [place_id]
        else:
            final_args = args
        return site_class(*final_args, **kwargs)

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

        Site classes for one-off scrapers should live in the *scrapers*
        namespace in a module named by state and county, e.g. *court_scraper.scrapers.ny_westchester*.

        Platform site classes should live in the *platforms* namespace
        (e.g. *court_scraper.platforms.odyssey*).

        In both cases, *sites_meta.csv* should specify the package name
        in the :code:`site_type` field as a snake_case value (e.g. *odyssey* or *wicourts*).

        """
        if place_id == site_type:
            parent_mod = 'scrapers'
        else:
            parent_mod = 'platforms'
        target_module = 'court_scraper.{}.{}'.format(parent_mod, site_type)
        mod = importlib.import_module(target_module)
        return getattr(mod, 'Site')
