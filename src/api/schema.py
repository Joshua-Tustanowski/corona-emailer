from typing import Optional
import datetime

from pydantic import BaseModel


class CountryBaseSchema(BaseModel):
    code: str


class CountryCreateSchema(CountryBaseSchema):
    id: int


class CountryReturnSchema(CountryBaseSchema):
    class Config:
        orm_mode = True


class CaseDataBaseSchema(BaseModel):
    country: CountryReturnSchema
    total_cases: int
    new_cases: int
    total_deaths: Optional[int]
    new_deaths: int
    active_cases: Optional[int]
    total_recovered: Optional[int]
    serious_critical: Optional[int]


class CaseDataReturnSchema(CaseDataBaseSchema):
    date_updated: datetime.datetime

    class Config:
        orm_mode = True
