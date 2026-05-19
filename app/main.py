from fastapi import FastAPI
from app.web import creature
from app.web import explorer
app = FastAPI()
app.include_router(creature.router)
app.include_router(explorer.router)