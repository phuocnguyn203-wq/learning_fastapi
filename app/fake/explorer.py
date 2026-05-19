from app.model.explorer import Explorer, ExplorerUpdate
from fastapi import HTTPException

_explorers = [
    Explorer(name='Johan',
             country='DE',
             description='idk'
             ),
    Explorer(name='Kursh',
             country='US',
             description='a harsh hunter',
             )
]

def get_one(name: str) -> Explorer | None:
    for explorer in _explorers:
        if explorer.name == name:
            return explorer
    return None

def get_all() -> list[Explorer]:
    return _explorers

def create(explorer: Explorer) -> Explorer:
    #create logic here
    #...
    return explorer

def modify(name: str, explorer_update: ExplorerUpdate) -> Explorer:
    old_explorer = get_one(name)
    if old_explorer is None:
        raise HTTPException(
            status_code=404,
            detail=f'Cant find explorer with name {name}',
        )
    #modify logic here
    #...
    old_explorer_dict = old_explorer.model_dump()
    update_explorer_dict = explorer_update.model_dump()
    old_explorer_dict.update(update_explorer_dict)
    return Explorer(**old_explorer_dict)

def replace(name, explorer: Explorer) -> Explorer:
    old_explorer = get_one(name)
    if not old_explorer:
        raise HTTPException(
            status_code=404,
            detail=f'Cant find explorer with name {name}',
        )
    #replace logic here
    #...
    return explorer

def delete(name: str) -> Explorer:
    explorer = get_one(name)
    if not explorer:
        raise HTTPException(
            status_code=404,
            detail=f'Cant find explorer with name {name}'
        )
    # delete logic here
    # ...
    return explorer