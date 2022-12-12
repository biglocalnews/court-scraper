import importlib
from datetime import datetime, timedelta

from court_scraper.configs import Configs
from court_scraper.sites_meta import SitesMeta


def dates_for_range(start_date, end_date, input_format="%Y-%m-%d", output_format=None):
    start = datetime.strptime(start_date, input_format)
    end = datetime.strptime(end_date, input_format)
    dates = []
    number_of_days = (end - start).days + 1
    for num in range(number_of_days):
        dt = start + timedelta(num)
        try:
            dates.append(dt.strftime(output_format))
        except TypeError:
            dates.append(dt)
    return dates


def get_captcha_service_api_key():
    configs = Configs()
    return configs.captcha_service_api_key


def get_runner(place_id):
    """Retrieve the runner for the provided place_id."""
    # Site types for one-off scrapers should live in the scrapers
    # namespace in a module named by state and county, e.g. ny_westchester.
    # Platform site classes should live in platforms namespace
    # in a snake_case module (e.g. odyssey).
    # In both cases, sites_meta.csv should specify the module name
    # in the site_type field as a snake_case value (ny_westchester, odyssey).
    meta = SitesMeta()
    site_type = meta.get(place_id)["site_type"]
    if place_id == site_type:
        parent_mod = "scrapers"
    else:
        parent_mod = "platforms"
    target_module = f"court_scraper.{parent_mod}.{site_type}.runner"
    mod = importlib.import_module(target_module)
    return getattr(mod, "Runner")
