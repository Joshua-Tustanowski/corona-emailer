from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


def create_dbsess():
    engine = create_engine('mysql://joshua:root@localhost/covid_data')
    Session = sessionmaker(bind=engine)
    return Session()


class Countries(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    code = Column(String(32), unique=True)


class CountryData(Base):
    __tablename__ = 'country_data'
    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('countries.id'))
    total_cases = Column(Integer, nullable=False)
    new_cases = Column(Integer, nullable=False)
    total_deaths = Column(Integer, nullable=True)
    new_deaths = Column(Integer, nullable=False)
    active_cases = Column(Integer, nullable=True)
    total_recovered = Column(Integer, nullable=True)
    serious_critical = Column(Integer, nullable=True)
    date_updated = Column(DateTime)

    country = relationship('Countries', backref='data')
