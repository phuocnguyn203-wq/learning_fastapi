from fastapi import APIRouter
from app.model.explorer import Explorer, ExplorerUpdate
from app.service import explorer as service

router = APIRouter(
    prefix='/explorer'
)

@router.get('/get_explorer/{name}')
def get_one(name: str) -> Explorer:
    return service.get_one(name)

@router.get('/all')
def get_all() -> list[Explorer]:
    return service.get_all()

@router.post('/create')
def create(explorer: Explorer) -> Explorer:
    return service.create(explorer)

@router.patch('/modify')
def modify_explorer(name: str, explorer_update: ExplorerUpdate) -> Explorer:
    return service.modify(name, explorer_update)

@router.delete('/delete')
def delete_explorer(name: str) -> Explorer:
    return service.delete(name)
