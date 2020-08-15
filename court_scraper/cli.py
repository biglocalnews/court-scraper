import logging
import os
import traceback
from pathlib import Path

import click
from click_option_group import optgroup, RequiredMutuallyExclusiveOptionGroup

from court_scraper.runner import Runner

try:
    CACHE_DIR = os.environ['COURT_SCRAPER_DIR']
except KeyError:
    CACHE_DIR = str(Path(os.path.expanduser('~')).joinpath('.court-scraper'))

CONFIG_PATH = str(Path(CACHE_DIR).joinpath('config.yaml'))



@click.command(
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
def cli(place_id, search_term, search_terms_file, with_browser):
    """Search court site."""
    # Ensure cache directory exists
    cache_dir = Path(CACHE_DIR)
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
    formatter = logging.Formatter('%(name)-12s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger(__name__)
    runner = Runner(
        CACHE_DIR,
        CONFIG_PATH,
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
    data = runner.search(**kwargs)
    # TODO: Do something with the data :)
    #traceback_str = ''.join(traceback.format_tb(e.__traceback__))
    #logger.error("ERROR: A fatal error occurred while running scraper!!!")
    #logger.error(traceback_str)
