import datetime as dt
from typing import Dict, List

from sqlalchemy.orm import Session

from datamanagers import get_all_daily_data
from .models import Countries, CountryData, create_dbsess


def populate_country_data(dbsess: Session) -> None:
    results = get_all_daily_data()
    for country, cases in results.items():
        if country != "":
            country_case_data = process_country_data(dbsess, country, cases)
            assert country_case_data, f"country case data is None for {country}"
            dbsess.add(country_case_data)
            try:
                dbsess.commit()
            except Exception as ex:
                print(ex)
                dbsess.rollback()


def process_country_data(
    dbsess: Session,
    country: str,
    country_data: List[str],
) -> CountryData:
    data = process_raw_data(country_data)
    res = CountryData(**data)
    res.date_updated = dt.datetime.utcnow()
    _country = dbsess.query(Countries).filter(Countries.code == country).one_or_none()
    assert _country, f"Country {country} does not exist"
    res.country_id = _country.id
    return res


def process_raw_data(country_data: List[str]) -> Dict[str, int]:
    _raw_data = list(
        map(lambda x: x.replace(",", "").replace("+", "").strip(), country_data),
    )
    _raw_data = [
        float(res) if (len(res) > 0 and res != "N/A") else 0 for res in _raw_data
    ]
    columns = [
        "total_cases",
        "new_cases",
        "total_deaths",
        "new_deaths",
        "active_cases",
        "total_recovered",
        "serious_critical",
        "date_updated",
    ]
    return {col: data for col, data in zip(columns, _raw_data)}


if __name__ == "__main__":
    dbsess = create_dbsess()
    populate_country_data(dbsess)
