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

    def upsert(self, cases):
        """
        Update or insert case data
        """
        session = Session()
        for case_data in cases:
            place_id = case_data.pop('place_id')
            number = case_data.pop('number')
            try:
                case_obj = session.query(Case)\
                        .filter_by(
                            place_id=place_id,
                            number=number)\
                        .one()
                # Update fields other than place_id and number
                for attr, val in case_data.items():
                    setattr(case_obj, attr, val)
            except NoResultFound:
                case_obj = Case(place_id=place_id, number=number, **case_data)
                session.add(case_obj)
        session.commit()
