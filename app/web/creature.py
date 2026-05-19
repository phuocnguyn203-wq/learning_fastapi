from fastapi import APIRouter
from app.model.creature import Creature, CreatureUpdate
from app.service import creature as service

router = APIRouter(
    prefix='/creature'
)

@router.get('/get_creature/{name}')
def get_one(name: str) -> Creature:
    return service.get_one(name)

@router.get('/all')
def get_all() -> list[Creature]:
    return service.get_all()

@router.post('/create')
def create(creature: Creature) -> Creature:
    return service.create(creature)

@router.patch('/modify_creature')
def modify_creature(name: str, creature: CreatureUpdate) -> Creature:
    return service.modify(name, creature)

@router.put('/replace')
def replace_creature(name: str, creature: Creature) -> Creature:
    return service.replace(name, creature)

@router.delete('/delete_creature')
def delete_creature(name: str) -> Creature:
    return service.delete(name)