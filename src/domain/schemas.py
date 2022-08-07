from pydantic import BaseModel
from typing import List


class CountryData(BaseModel):
    id: int
    name: str


class CountryList(BaseModel):
    countries: List[CountryData]
