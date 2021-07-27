from os.path import expanduser
import shutil
from pathlib import Path

import pytest
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


# NOTE: To check if vcrpy/pytest-vcr
# is using cassettes as opposed to making
# live web requests, uncomment below
# and pass pytest caplog fixture to
# a test function. More details here:
#    https://vcrpy.readthedocs.io/en/latest/debugging.html
# import vcr
# import logging
# Initialize logging in order see output from vcrpy
# logging.basicConfig()
# vcr_log = logging.getLogger("vcr")
# vcr_log.setLevel(logging.INFO)

def get_live_configs(home=expanduser("~")):
    try:
        config_path = Path(home, '.court-scraper/config.yaml')
    except KeyError:
        return ''
    with open(config_path,'r') as fh:
        return yaml.load(fh, Loader=Loader)

def load_yaml(path):
    with open(path, 'r') as fh:
        return yaml.load(fh, Loader=Loader)

try:
    CAPTCHA_API_KEY = get_live_configs()['captcha_service_api_key']
except:
    CAPTCHA_API_KEY = None

def pytest_addoption(parser):
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )
    parser.addoption(
        "--headless", action="store_true", default=False,
        help="Run live webtests in headless mode"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")
    config.addinivalue_line("markers", "webtest: mark test as hitting live websites")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


@pytest.fixture
def headless(request):
    return request.config.getoption("--headless")


@pytest.fixture
def live_configs():
    return get_live_configs()

@pytest.fixture
def court_scraper_dir(tmp_path):
    return str(
        tmp_path.joinpath('court-scraper')
    )


@pytest.fixture
def config_path(tmp_path):
    return str(
        tmp_path.joinpath('court-scraper/config.yaml')
    )


@pytest.fixture
def db_path(court_scraper_dir):
    return str(
        Path(court_scraper_dir).joinpath('cases.db')
    )


@pytest.fixture
def create_scraper_dir(court_scraper_dir):
    Path(court_scraper_dir).mkdir(parents=True, exist_ok=True)


@pytest.fixture
def create_config(config_path):
    config_fixture = Path(__file__)\
        .parent\
        .joinpath('fixtures/config.yaml')
    shutil.copyfile(config_fixture, config_path)


def update_test_configs(config_path, data):
    configs = load_yaml(config_path)
    configs.update(data)
    with open(config_path,'w') as fh:
        return yaml.dump(configs, fh, Dumper=Dumper)


@pytest.fixture(autouse=True)
def set_env(court_scraper_dir, monkeypatch):
    monkeypatch.setenv(
        'COURT_SCRAPER_DIR',
        court_scraper_dir
    )


def read_fixture(file_name):
    path = str(
        Path(__file__)\
            .parent\
            .joinpath('fixtures')\
            .joinpath(file_name)
    )
    return file_contents(path)


def file_contents(pth):
    with open(pth, 'r') as f:
        return f.read()


@pytest.fixture
def case_data():
    return [
        {'place_id': 'ga_dekalb', 'case_num': '1'},
        {'place_id': 'ga_dekalb', 'case_num': '2'},
    ]


@pytest.fixture
def optional_case_data():
    return [
        {
            'place_id': 'ga_dekalb',
            'case_num': '1',
            'status': 'Open',
            'filing_date': '01/02/2019',
        },
        {
            'place_id': 'ga_dekalb',
            'case_num': '2',
            'status': 'Closed',
            'filing_date': '03/04/2019',
        }
    ]


@pytest.fixture
def required_case_data():
    return [
        {
            'place_id': 'ga_dekalb',
            'number': '1',
            'status': 'Open',
        },
        {
            'place_id': 'ga_dekalb',
            'number': '2',
            'status': 'Closed',
        }
    ]

@pytest.fixture
def sites_csv_text():
    return read_fixture('sites_meta.csv')
