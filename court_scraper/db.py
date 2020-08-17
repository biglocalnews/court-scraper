from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,String,
    UniqueConstraint
)

Base = declarative_base()


class Case(Base):
    __tablename__ = 'cases'

    id = Column(Integer, primary_key=True)
    place_id = Column(String)
    number = Column(String)

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
