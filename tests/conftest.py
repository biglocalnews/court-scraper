from pathlib import Path

import pytest


@pytest.fixture
def court_scraper_dir(tmp_path):
    return str(
        tmp_path.joinpath('court-scraper-scraper')
    )

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
