import importlib
import typing
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


def get_runner(place_id: str):
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


def get_runners_in_state(postal_code: str) -> typing.List:
    """Retrieve the runners in the provided state."""
    meta = SitesMeta()
    site_list = meta.get_state_list(postal_code)
    runner_list = []
    for site in site_list:
        runner = get_runner(site["place_id"])
        runner_list.append(runner)
    return runner_list


def get_site_meta(place_id: str):
    """Retrieve the metadata for the provided site."""
    sm = SitesMeta()
    state = place_id[0:2]
    county = place_id[3:].replace("_", " ").strip()
    return sm.data[(state, county)]


def get_site_class(place_id: str, site_type: str):
    """Look up Site class by place ID and site type.

    Site classes for one-off scrapers should live in the *scrapers*
    namespace in a module named by state and county, e.g. *court_scraper.scrapers.ny_westchester*.

    Platform site classes should live in the *platforms* namespace
    (e.g. *court_scraper.platforms.odyssey*).

    In both cases, *sites_meta.csv* should specify the package name
    in the :code:`site_type` field as a snake_case value (e.g. *odyssey* or *wicourts*).
    """
    if place_id == site_type:
        parent_mod = "scrapers"
    else:
        parent_mod = "platforms"
    target_module = f"court_scraper.{parent_mod}.{site_type}"
    mod = importlib.import_module(target_module)
    return getattr(mod, "Site")
