from fastapi import HTTPException
from app.data.init import conn, curs
from app.model.creature import Creature, CreatureUpdate
from sqlite3 import IntegrityError
from pydantic import BaseModel

TABLE_NAME = 'creature'


curs.execute(f"""
             create table if not exists {TABLE_NAME}(
                 name text primary key,
                 description text,
                 country text,
                 area text)"""
                 )

def row_to_model(row: tuple) -> Creature:
    (name, description, country, area) = row
    return Creature(
        name=name,
        description=description,
        country=country,
        area=area
    )

def model_to_dict(model: BaseModel) -> dict:
    return model.model_dump()

def get_one(name: str) -> Creature:
    qry = f'select * from {TABLE_NAME} where name = :name'
    params = {'name': name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if not row:
        raise HTTPException(
            status_code=404,
            detail=f'Cant find creature with name {name}',
        )
    return row_to_model(row)

def get_all() -> list[Creature]:
    qry = f'select * from {TABLE_NAME}'
    curs.execute(qry)
    all_creatures = curs.fetchall()
    if not all_creatures:
        raise HTTPException(
            status_code=404,
            detail='No creature',
        )
    return [row_to_model(creature) for creature in all_creatures]

def create(creature: Creature) -> Creature:
    
    qry = f'''
    insert into {TABLE_NAME} values
    (:name, :description, :country, :area)'''
    params = model_to_dict(creature)
    try:
        curs.execute(qry, params)
        conn.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail='This creature already exists',
        )
    return get_one(creature.name)

def modify(name: str, creature_update: CreatureUpdate) -> Creature:
    old_creature = get_one(name)
    if not old_creature:
        raise HTTPException(
            status_code=404,
            detail=f'Cant find creature with name {name}',
        )
    qry = '''
    update creature set 
    country=:country
    name=:name
    description=:description
    area=:area
    where name=:old_name'''
    
    old_creature_dict = model_to_dict(old_creature)
    creature_update_dict = model_to_dict(creature_update)
    old_creature_dict.update(**creature_update_dict)
    old_creature_dict['old_name'] = name
    curs.execute(qry, old_creature_dict)
    
    return get_one(name)

def delete(name: str) -> Creature:
    creature = get_one(name)
    if not creature:
        raise HTTPException(
            status_code=404,
            detail=f'Cant find creature with name {name}',
        )
    qry = f'''delete from {TABLE_NAME} where name =: name'''
    params = {'name': name}
    curs.execute(qry, params)
    return creature
    