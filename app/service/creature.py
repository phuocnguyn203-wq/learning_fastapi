from app.model.creature import Creature, CreatureUpdate
from app.data import creature as creature_data

def get_one(name: str) -> Creature:
    return creature_data.get_one(name)

def get_all() -> list[Creature]:
    return creature_data.get_all()
def create(creature: Creature) -> Creature:
    return creature_data.create(creature)

def modify(name: str, creature_update: CreatureUpdate) -> Creature:
    return creature_data.modify(name, creature_update)

def delete(name: str) -> Creature:
    return creature_data.delete(name)