from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from .db import Base, Case


Session = sessionmaker()


class Datastore:

    def __init__(self, path):
        self.db_path = path
        self.engine = create_engine(
            'sqlite:///{}'.format(path)
        )
        Base.metadata.create_all(self.engine)
        Session.configure(bind=self.engine)

    def add(self, cases):
        """
        Adds case data to db if it doesn't
        already exist.
        """
        session = Session()
        for c in cases:
            kwargs = {
                'place_id': c['place_id'],
                'number': c['case_num'],
            }
            try:
                case_obj = session.query(Case).filter_by(**kwargs).one()
            except NoResultFound:
                case_obj = Case(**kwargs)
                session.add(case_obj)
        session.commit()
