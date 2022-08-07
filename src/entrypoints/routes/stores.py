from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.adapters.orm import get_db
from src.handlers.stores import StoresHandler
from src.domain import schemas

router = APIRouter(
    prefix="/stores",
    tags=["Stores"],
    responses={404: {"description": "Not found"}},
)


@router.post("", status_code=200, response_model=schemas.StoreData)
async def create_store(new_store: schemas.StoreCreate, db: Session = Depends(get_db)):
    store_handler = StoresHandler(db)
    store = await store_handler.create_store(new_store)
    response = schemas.StoreData(
        id=store.id,
        country_id=store.country_id,
        tax_id=store.tax_id,
        name=store.name,
        legal_name=store.legal_name,
        address=store.address,
        zip_code=store.zip_code,
        email=store.email,
        phone=store.phone,
        active=store.active,
    )
    return response
