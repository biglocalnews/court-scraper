from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    event,
    DateTime,
    Column,
    Integer,
    String,
    UniqueConstraint
)


# Source for timestamp mixin cribbed from
# https://sqlalchemy-utils.readthedocs.io/en/latest/_modules/sqlalchemy_utils/models.html#Timestamp
class TimestampMixin:
    created = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated = Column(DateTime, default=datetime.utcnow, nullable=False)


@event.listens_for(TimestampMixin, 'before_update', propagate=True)
def timestamp_before_update(mapper, connection, target):
    target.updated = datetime.utcnow()


Base = declarative_base()


class Case(Base, TimestampMixin):
    __tablename__ = 'cases'

    id = Column(Integer, primary_key=True)
    place_id = Column(String, nullable=False)
    number = Column(String, nullable=False)
    filing_date = Column(String)
    status = Column(String)
    UniqueConstraint(
        'place_id',
        'number',
        name='uix_place_id_case_num'
    )

    def __repr__(self):
        return '<Case(id={}, place_id={}, case_num={})> '.format(
            self.id,
            self.place_id,
            self.number
        )
