from pydantic import BaseModel
from typing import List


class CountryData(BaseModel):
    id: int
    name: str


class CountriesList(BaseModel):
    countries: List[CountryData]


class RolData(BaseModel):
    id: int
    name: str


class RolesList(BaseModel):
    roles: List[RolData]
