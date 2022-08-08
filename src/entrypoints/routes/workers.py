from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.adapters.orm import get_db
from src.handlers.workers import WorkersHandler
from src.handlers.stores import StoresHandler
from src.domain import schemas


router = APIRouter(
    prefix="/workers",
    tags=["Workers"],
    responses={404: {"description": "Not found"}},
)


@router.post("", status_code=200, response_model=schemas.WorkerData)
async def create_worker(new_worker: schemas.WorkerCreate, db: Session = Depends(get_db)):
    store_handler = StoresHandler(db)
    store = await store_handler.get_store(new_worker.store_id)
    if not store.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The store is not active",
        )
    worker_handler = WorkersHandler(db)
    worker = await worker_handler.create_worker(new_worker)
    response = schemas.WorkerData(
        user_id=worker.user_id,
        store_id=worker.store_id,
        store_name=worker.store.name,
        rol_id=worker.rol_id,
        rol_name=worker.rol.name,
        active=worker.active,
    )
    return response


@router.get("", status_code=200, response_model=schemas.WorkersList)
async def get_workers(page: int = 1, per_page: int = 10, store_id: int = 1, db: Session = Depends(get_db)):
    worker_handler = WorkersHandler(db)
    workers = await worker_handler.get_workers(page, per_page, store_id)
    workers_list = [
        schemas.WorkerBasicData(
            user_id=worker.user_id,
            rol_id=worker.rol_id,
            rol_name=worker.rol.name,
            active=worker.active,
        )
        for worker in workers
    ]
    try:
        response = schemas.WorkersList(
            store_id = store_id,
            store_name=workers[0].store.name,
            workers=workers_list
        )
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The store does not have workers",
        )
    return response


@router.get("/{store_id}/{user_id}", status_code=200, response_model=schemas.WorkerData)
async def get_worker(store_id: int, user_id: int, db: Session = Depends(get_db)):
    worker_handler = WorkersHandler(db)
    worker = await worker_handler.get_worker(store_id, user_id)
    response = schemas.WorkerData(
        user_id=worker.user_id,
        store_id=worker.store_id,
        store_name=worker.store.name,
        rol_id=worker.rol_id,
        rol_name=worker.rol.name,
        active=worker.active,
    )
    return response
