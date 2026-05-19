from fastapi import HTTPException
from app.model.creature import Creature, CreatureUpdate
_creatures = [
    Creature(
        name='Kuttaki',
        country='JP',
        description='A bird with teleport quirk',
        area='A',
    ),
    Creature(
        name='Rork',
        country='Denmark',
        description='Old dog',
        area='C',
    )
]

def get_one(name: str) -> Creature:
    for creature in _creatures:
        if creature.name == name:
            return creature
    raise HTTPException(
        status_code=404,
        detail=f'Cant find creature with name {name}',
    )

def get_all() -> list[Creature]:
    if len(_creatures) == 0:
        raise HTTPException(
            status_code=404,
            detail='nothing to retriever',
        )
    return _creatures

def create(creature: Creature) -> Creature:
    #create logic here
    #...
    return creature

def modify(name: str, creature_update: CreatureUpdate) -> Creature:
    old_creature = get_one(name)
    if not old_creature:
        raise HTTPException(
            status_code=404,
            detail=f'Cant find creature with name {name}',
        )
    old_creature_dict = old_creature.model_dump()
    creature_update_dict = creature_update.model_dump()
    old_creature_dict.update(creature_update_dict)
    return Creature(**old_creature_dict)

def replace(name: str, creature: Creature) -> Creature:
    old_creature = get_one(name)
    if not old_creature:
        raise HTTPException(
            status_code=404,
            detail=f'Cant find creature with name {name}',
        )
    #replace logic here
    return creature

def delete(name: str) -> Creature:
    old_creature = get_one(name)
    if not old_creature:
        raise HTTPException(
            status_code=404,
            detail=f'Cant find creature with name {name}',
        )
    return old_creature