from pydantic import BaseModel, EmailStr
from typing import List, Optional


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


class StoreCreate(BaseModel):
    country_id: int
    tax_id: str
    name: str
    legal_name: str
    address: str
    zip_code: str
    email: EmailStr
    phone: Optional[str] = None


class StoreData(BaseModel):
    id: int
    country_id: int
    tax_id: str
    name: str
    legal_name: str
    address: str
    zip_code: str
    email: EmailStr
    phone: Optional[str] = None
    active: bool = True


class StoresList(BaseModel):
    stores: List[StoreData]
