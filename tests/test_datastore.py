from datetime import datetime
from pathlib import Path
import pytest

from court_scraper.datastore import Datastore, Session
from court_scraper.db import Case

from .conftest import db_path, case_data, optional_case_data


@pytest.mark.usefixtures('create_scraper_dir')
def test_add(db_path, case_data):
    store = Datastore(db_path)
    store.add(case_data)
    cases = Session().query(Case).all()
    assert len(cases) == 2


@pytest.mark.usefixtures('create_scraper_dir')
def test_timestamp(db_path, case_data):
    store = Datastore(db_path)
    store.add(case_data)
    cases = Session().query(Case).all()
    for case in cases:
        assert isinstance(case.created, datetime)
