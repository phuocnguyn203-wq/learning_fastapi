from typing import Optional
from pydantic import BaseModel

class Explorer(BaseModel):
    name: str
    country: str
    description: str

class ExplorerUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    description: Optional[str] = None