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
        rol_id=worker.rol_id,
    )
    return response