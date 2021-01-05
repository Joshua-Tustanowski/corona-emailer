from typing import List

from sqlalchemy.orm import Session

from db import CountryData, Countries


def get_todays_data(db: Session, limit: int) -> List[CountryData]:
    return db.query(CountryData).filter(CountryData.date_updated).limit(limit).all()


def get_yesterdays_data(db: Session):
    return db.query(CountryData).filter(CountryData.date_updated).all()


def get_data_by_country(db: Session, country_code: str):
    country = db.query(Countries).filter(Countries.code == country_code).one_or_none()
    todays_country_result = (
        db.query(CountryData).filter(CountryData.country == country).one_or_none()
    )
    return todays_country_result
