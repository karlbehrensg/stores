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


@router.get("", status_code=200, response_model=schemas.StoresList)
async def get_stores(page: int = 1, per_page: int = 10, db: Session = Depends(get_db)):
    store_handler = StoresHandler(db)
    stores = await store_handler.get_stores(page, per_page)
    stores_list = [
        schemas.StoreData(
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
        for store in stores
    ]
    response = schemas.StoresList(stores=stores_list)
    return response


@router.get("/{store_id}", status_code=200, response_model=schemas.StoreData)
async def get_store(store_id: int, db: Session = Depends(get_db)):
    store_handler = StoresHandler(db)
    store = await store_handler.get_store(store_id)
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


@router.put("/{store_id}", status_code=200, response_model=schemas.StoreData)
async def update_store(
    store_id: int, data: schemas.StoreUpdate, db: Session = Depends(get_db)
):
    store_handler = StoresHandler(db)
    store = await store_handler.update_store(store_id, data)
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


@router.delete("/{store_id}", status_code=200, response_model=schemas.StoreData)
async def deactivate_store(store_id: int, db: Session = Depends(get_db)):
    store_handler = StoresHandler(db)
    store = await store_handler.deactivate_store(store_id)
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


@router.post("/{store_id}/activate", status_code=200, response_model=schemas.StoreData)
async def activate_store(store_id: int, db: Session = Depends(get_db)):
    store_handler = StoresHandler(db)
    store = await store_handler.activate_store(store_id)
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
