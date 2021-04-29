import logging
import os
import traceback
from pathlib import Path

import click
from click_option_group import optgroup, RequiredMutuallyExclusiveOptionGroup

from court_scraper.configs import Configs
from court_scraper.datastore import Datastore
from court_scraper.runner import Runner
from court_scraper.sites_meta import SitesMeta

configs = Configs()
cache_dir = Path(configs.cache_dir)
cache_dir.mkdir(parents=True, exist_ok=True)
log_file = str(cache_dir.joinpath('logfile.txt'))
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)-12s - %(message)s',
    datefmt='%m-%d %H:%M',
    filename=log_file,
    filemode='a'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
logger = logging.getLogger(__name__)



@click.group()
def cli():
    pass


@cli.command(
    help="Search and scrape case info from county court site."
)
@click.option(
    '-p',
    '--place-id',
    required=True,
    help="A unique place ID made up of the state and county (e.g. ga_dekalb)"
)
@optgroup.group(
    'Search term sources',
    cls=RequiredMutuallyExclusiveOptionGroup,
    help='Search terms must be supplied on the command line or via text file.'
)
@optgroup.option(
    '-s',
    '--search-term',
    help="A search term."
)
@optgroup.option(
    '-f',
    '--search-terms-file',
    type=click.File('r'),
    help="Text file containing one or more search terms."
)
@click.option(
    '--with-browser',
    is_flag=True,
    help="Open graphical browser during Selenium-based scrapes. By default, runs headless."
)
def search(place_id, search_term, search_terms_file, with_browser):
    """Search court site."""
    runner = Runner(
        configs.cache_dir,
        configs.config_file_path,
        place_id
    )
    if search_term:
        search_terms = [search_term]
    else:
        search_terms = [t.strip() for t in search_terms_file]
    kwargs = {
        'search_terms': search_terms,
        'headless': not with_browser,
    }
    # TODO: Restore catch-all try/except
    results = runner.search(**kwargs)
    runner.cache_detail_pages(results)
    dstore = Datastore(configs.db_path)
    logger.info(
        "Adding {} results to {}".format(len(results), configs.db_path)
    )
    to_db = []
    for result in results:
        # Place ID is required Case db table
        result.place_id = place_id
        to_db.append(result.standard_data)
    dstore.upsert(to_db)
    #traceback_str = ''.join(traceback.format_tb(e.__traceback__))
    #logger.error("ERROR: A fatal error occurred while running scraper!!!")
    #logger.error(traceback_str)


@cli.command(help="Get info about available scrapers")
def info():
    msg = "\nAvailable scrapers:\n\n"
    meta = SitesMeta()
    for state, county in meta.data.keys():
        entry = " * {} - {} ({})\n".format(
            state.upper(),
            county.title(),
            '_'.join((state, county.replace(' ', '_')))
        )
        msg += entry
    end_note = "\nNOTE: Scraper IDs (in parentheses) should be " +\
        "used with the search command's --place-id argument."
    msg += end_note
    click.echo(msg)
