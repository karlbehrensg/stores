from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.adapters.orm import get_db
from src.handlers.countries import CountriesHandler
from src.domain import schemas

router = APIRouter(
    prefix="/countries",
    tags=["Countries"],
    responses={404: {"description": "Not found"}},
)


@router.get("", status_code=200, response_model=schemas.CountriesList)
async def get_countries(db: Session = Depends(get_db)):
    country_handler = CountriesHandler(db)
    countries = await country_handler.get_countries()
    response = schemas.CountriesList(countries=countries)
    return response
