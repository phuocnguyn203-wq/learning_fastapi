from fastapi import HTTPException
from app.data.init import conn, curs
from app.model.explorer import Explorer, ExplorerUpdate
from sqlite3 import IntegrityError
from pydantic import BaseModel

TABLE_NAME = 'explorer'


curs.execute(f"""
             create table if not exists {TABLE_NAME}(
                 name text primary key,
                 country text,
                 description text)"""
                 )
conn.commit()

def row_to_model(row: tuple) -> Explorer:
    (name, country, description) = row
    return Explorer(
        name=name,
        country=country,
        description=description
    )

def model_to_dict(model: BaseModel, exclude_none: bool = False) -> dict:
    return model.model_dump(exclude_none=exclude_none)

def get_one(name: str) -> Explorer:
    qry = f'select * from {TABLE_NAME} where name = :name'
    params = {'name': name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if not row:
        raise HTTPException(
            status_code=404,
            detail=f'Cant find explorer with name {name}',
        )
    return row_to_model(row)

def get_all() -> list[Explorer]:
    qry = f'select * from {TABLE_NAME}'
    curs.execute(qry)
    all_explorers = curs.fetchall()
    if not all_explorers:
        raise HTTPException(
            status_code=404,
            detail='No explorer',
        )
    return [row_to_model(explorer) for explorer in all_explorers]

def create(explorer: Explorer) -> Explorer:
    qry = f'''
    insert into {TABLE_NAME}
    (name, country, description)
    values
    (:name, :country, :description)'''
    params = model_to_dict(explorer)
    try:
        curs.execute(qry, params)
        conn.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail='This explorer already exists',
        )
    return get_one(explorer.name)

def modify(name: str, explorer_update: ExplorerUpdate) -> Explorer:
    old_explorer = get_one(name)
    old_explorer_dict = model_to_dict(old_explorer)
    explorer_update_dict = model_to_dict(explorer_update, exclude_none=True)

    if not explorer_update_dict:
        raise HTTPException(
            status_code=400,
            detail=f'No explorer with name {name}',
        )

    old_explorer_dict.update(explorer_update_dict)
    old_explorer_dict['old_name'] = name

    qry = f'''
    update {TABLE_NAME} set
    name=:name,
    country=:country,
    description=:description
    where name=:old_name'''

    try:
        curs.execute(qry, old_explorer_dict)
        conn.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail='This explorer already exists',
        )

    return get_one(old_explorer_dict['name'])

def delete(name: str) -> Explorer:
    explorer = get_one(name)
    qry = f'delete from {TABLE_NAME} where name = :name'
    params = {'name': name}
    curs.execute(qry, params)
    conn.commit()
    return explorer
