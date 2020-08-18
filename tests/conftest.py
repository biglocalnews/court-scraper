import shutil
from pathlib import Path

import pytest


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
