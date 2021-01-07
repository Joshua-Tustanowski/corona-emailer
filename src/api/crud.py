from typing import List
import datetime as dt

from sqlalchemy.orm import Session

from db import CountryData, Countries


def get_todays_data(db: Session, limit: int) -> List[CountryData]:
    return (
        db.query(CountryData)
        .filter(CountryData.date_updated >= dt.date.today())
        .limit(limit)
        .all()
    )


def get_yesterdays_data(db: Session):
    return db.query(CountryData).filter(CountryData.date_updated).all()


def get_data_by_country(
    db: Session, country_code: str, look_back: str
) -> List[CountryData]:
    country = db.query(Countries).filter(Countries.code == country_code).one_or_none()
    look_back = dt.date.today() if look_back is None else look_back
    todays_country_result = (
        db.query(CountryData)
        .filter(CountryData.country == country, CountryData.date_updated >= look_back)
        .all()
    )
    return todays_country_result
