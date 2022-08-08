from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.adapters.orm import get_db
from src.handlers.roles import RolesHandler
from src.domain import schemas

router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
    responses={404: {"description": "Not found"}},
)


@router.get("", status_code=200, response_model=schemas.RolesList)
async def get_roles(db: Session = Depends(get_db)):
    roles_handler = RolesHandler(db)
    roles = await roles_handler.get_roles()
    response = schemas.RolesList(roles=roles)
    return response
