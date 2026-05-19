from typing import Optional
from pydantic import BaseModel

class Creature(BaseModel):
    name: str
    country: str
    description: str
    area: str

class CreatureUpdate(BaseModel):
    country: Optional[str] = None
    description: Optional[str] = None
    area: Optional[str] = None
