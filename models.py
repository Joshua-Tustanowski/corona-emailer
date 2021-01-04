from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('mysql://joshua:root@localhost/covid_data', echo=True)

Session = sessionmaker(bind=engine)
session = Session()


class Countries(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    code = Column(String(10))


class CountryData(Base):
    __tablename__ = 'country_data'
    id = Column(Integer, primary_key=True)
    country_id = Column(ForeignKey('countries.id'))
    total_cases = Column(Integer, nullable=False)
    new_cases = Column(Integer, nullable=False)
    total_deaths = Column(Integer)
    new_deaths = Column(Integer, nullable=False)
    active_cases = Column(Integer)
    total_recovered = Column(Integer)
    serious_critical = Column(Integer)
    date_updated = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    country = relationship('Countries', backref='data')
