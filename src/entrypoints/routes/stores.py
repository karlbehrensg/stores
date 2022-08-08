from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from src.adapters.orm import get_db
from src.handlers.stores import StoresHandler
from src.handlers.workers import WorkersHandler
from src.domain import schemas
from src.utils.validatetion import validate_rol

router = APIRouter(
    prefix="/stores",
    tags=["Stores"],
    responses={404: {"description": "Not found"}},
)


@router.post("", status_code=200, response_model=schemas.StoreData)
async def create_store(
    new_store: schemas.StoreCreate,
    current_user_id: int = Header(default=None, convert_underscores=True),
    db: Session = Depends(get_db),
):
    if not isinstance(current_user_id, int):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user id is not valid",
        )
    store_handler = StoresHandler(db)
    store = await store_handler.create_store(new_store)
    worker_handler = WorkersHandler(db)
    new_worker = schemas.WorkerCreate(
        user_id=current_user_id,
        store_id=store.id,
        rol_id=1,
    )
    await worker_handler.create_worker(new_worker)
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
async def get_stores(
    page: int = 1,
    per_page: int = 10,
    superuser: bool = Header(default=False),
    db: Session = Depends(get_db),
):
    if not superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The user is not authorized",
        )
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
async def get_store(
    store_id: int,
    current_user_id: int = Header(default=None, convert_underscores=True),
    superuser: bool = Header(default=False),
    db: Session = Depends(get_db),
):
    worker_handler = WorkersHandler(db)
    rol_condition = await validate_rol(
        worker_handler=worker_handler,
        store_id=store_id,
        user_id=current_user_id,
        accepted_roles_list=[1, 2],
    ) if not superuser else superuser

    if rol_condition:
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

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="The user is not authorized",
    )


@router.put("/{store_id}", status_code=200, response_model=schemas.StoreData)
async def update_store(
    store_id: int,
    data: schemas.StoreUpdate,
    current_user_id: int = Header(default=None, convert_underscores=True),
    superuser: bool = Header(default=False),
    db: Session = Depends(get_db),
):
    worker_handler = WorkersHandler(db)
    rol_condition = await validate_rol(
        worker_handler=worker_handler,
        store_id=store_id,
        user_id=current_user_id,
        accepted_roles_list=[1, 2],
    ) if not superuser else superuser

    if rol_condition:
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

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="The user is not authorized",
    )


@router.delete("/{store_id}", status_code=200, response_model=schemas.StoreData)
async def deactivate_store(
    store_id: int,
    current_user_id: int = Header(default=None, convert_underscores=True),
    superuser: bool = Header(default=False),
    db: Session = Depends(get_db),
):
    worker_handler = WorkersHandler(db)
    rol_condition = await validate_rol(
        worker_handler=worker_handler,
        store_id=store_id,
        user_id=current_user_id,
        accepted_roles_list=[1],
    ) if not superuser else superuser

    if rol_condition:
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

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="The user is not authorized",
    )


@router.post("/{store_id}/activate", status_code=200, response_model=schemas.StoreData)
async def activate_store(
    store_id: int,
    superuser: bool = Header(default=False),
    db: Session = Depends(get_db),
):
    if not superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The user is not authorized",
        )

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
