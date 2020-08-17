from pathlib import Path
import pytest

from court_scraper.datastore import Datastore, Session
from court_scraper.db import Case

from .conftest import db_path


@pytest.mark.usefixtures('create_scraper_dir')
def test_add(db_path):
    data = [
        {'place_id': 'ga_dekalb', 'case_num': '1'},
        {'place_id': 'ga_dekalb', 'case_num': '2'},
    ]
    store = Datastore(db_path)
    store.add(data)
    cases = Session().query(Case).all()
    assert len(cases) == 2
