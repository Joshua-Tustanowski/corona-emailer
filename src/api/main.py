from http import HTTPStatus
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from db import create_dbsess
from .crud import (
    get_data_by_country,
    get_todays_data,
)
from .schema import CaseDataReturnSchema

app = FastAPI()


def get_db():
    db = create_dbsess()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def hello_world():
    return {"message": "Hello, welcome to my COVID-19 data API"}


@app.get("/cases", response_model=List[CaseDataReturnSchema])
def get_todays_covid_data(db: Session = Depends(get_db), limit: int = 100):
    return get_todays_data(db, limit)


@app.get("/cases/{country_code}", response_model=CaseDataReturnSchema)
def get_todays_covid_data_for_country(country_code: str, db: Session = Depends(get_db)):
    country_cases = get_data_by_country(db, country_code)
    if country_cases is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"No case data found for {country_code}",
        )
    return country_cases
