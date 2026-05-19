from app.model.explorer import Explorer, ExplorerUpdate
from app.data import explorer as explorer_data

def get_one(name: str) -> Explorer:
    return explorer_data.get_one(name)

def get_all() -> list[Explorer]:
    return explorer_data.get_all()

def create(explorer: Explorer) -> Explorer:
    return explorer_data.create(explorer)

def modify(name: str, explorer_update: ExplorerUpdate) -> Explorer:
    return explorer_data.modify(name, explorer_update)

def delete(name: str) -> Explorer:
    return explorer_data.delete(name)
