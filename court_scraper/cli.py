import logging
import os
import traceback
from pathlib import Path

import click
from click_option_group import optgroup, RequiredMutuallyExclusiveOptionGroup
#from court_scraper.cli.custom_options import MutuallyExclusiveOption

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
    '-l',
    '--list-scrapers',
    is_flag=True,
    help="List available scrapers."
)
@click.option(
    '--headless/--with-browser',
    default=True,
    show_default="--headless",
    help="Enable/disable headless mode for Selenium-based browser scraping."
)
def cli(place_id, search_term, search_terms_file, list_scrapers, headless):
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
    """
    if list_scrapers:
        click.echo('Available scrapers:')
        #TODO: Add help message specifying that scraper code
        # (e.g. ga_fulton) must be used when scraping
        for scraper in runner.list_scrapers():
            msg = '- {}'.format(scraper)
            click.echo(msg)
    """
    if search_term:
        search_terms = [search_term]
    else:
        search_terms = [t.strip() for t in search_terms_file]
    kwargs = {
        'search_terms': search_terms,
        'headless': headless,
    }
    try:
        data = runner.search(**kwargs)
        print(data)
    except Exception as e:
        traceback_str = ''.join(traceback.format_tb(e.__traceback__))
        logger.error("ERROR: A fatal error occurred while running scraper!!!")
        logger.error(traceback_str)

