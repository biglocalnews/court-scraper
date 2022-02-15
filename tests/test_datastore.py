import pytest
from datetime import datetime
from court_scraper.datastore import Datastore, Session
from court_scraper.db import Case


@pytest.mark.usefixtures("create_scraper_dir")
def test_upsert(db_path, required_case_data):
    store = Datastore(db_path)
    store.upsert(required_case_data)
    cases = Session().query(Case).all()
    assert len(cases) == 2


@pytest.mark.usefixtures("create_scraper_dir")
def test_timestamp(db_path, required_case_data):
    store = Datastore(db_path)
    store.upsert(required_case_data)
    cases = Session().query(Case).all()
    for case in cases:
        assert isinstance(case.created, datetime)
