from fastapi import HTTPException, status
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.domain import schemas
from src.domain.models import Store


class StoresHandler:
    not_found_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Store not found",
    )

    def __init__(self, db: Session) -> None:
        self.db = db

    async def create_store(self, store: schemas.StoreCreate):
        try:
            new_store = Store(
                country_id=store.country_id,
                tax_id=store.tax_id,
                name=store.name,
                legal_name=store.legal_name,
                address=store.address,
                zip_code=store.zip_code,
                email=store.email,
                phone=store.phone,
            )
            self.db.add(new_store)
            self.db.commit()
            self.db.refresh(new_store)
            return new_store
        except (IntegrityError, UniqueViolation):
            raise HTTPException(
                status_code=400,
                detail="An error occurred: the store already exists or the country is not valid",
            )

    async def get_stores(self, page: int, per_page: int):
        stores = (
            self.db.query(Store).offset(per_page * (page - 1)).limit(per_page).all()
        )
        return stores

    async def get_store(self, store_id: int):
        store = self.db.query(Store).get(store_id)
        if store is None:
            raise self.not_found_exception
        return store

    async def update_store(self, store_id: int, data: schemas.StoreUpdate):
        store = self.db.query(Store).get(store_id)
        if store is None:
            raise self.not_found_exception
        store.name = data.name
        store.legal_name = data.legal_name
        store.address = data.address
        store.zip_code = data.zip_code
        store.email = data.email
        store.phone = data.phone
        self.db.add(store)
        self.db.commit()
        self.db.refresh(store)
        return store

    async def deactivate_store(self, store_id: int):
        store = self.db.query(Store).get(store_id)
        if store is None:
            raise self.not_found_exception
        store.active = False
        self.db.add(store)
        self.db.commit()
        self.db.refresh(store)
        return store
    
    async def activate_store(self, store_id: int):
        store = self.db.query(Store).get(store_id)
        if store is None:
            raise self.not_found_exception
        store.active = True
        self.db.add(store)
        self.db.commit()
        self.db.refresh(store)
        return store
