import os

from database import models, database
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import git_scripts
from routes import user
from routes import crew
from routes import tasks
from routes import todo
from routes import flash_cards
from routes import flash_card_deck

# docker run --name my-postgres-db -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydatabase -p 5432:5432 -d postgres
# start FastAPI
app = FastAPI()

app.include_router(git_scripts.router, prefix="/git", tags=["Git"])
app.include_router(user.router, prefix="/user", tags=["Users"])
app.include_router(crew.router, prefix="/crew", tags=["Crews"])
app.include_router(tasks.router, prefix="/task", tags=["Tasks"])
app.include_router(todo.router, prefix="/todo", tags=["Todos"])
app.include_router(flash_cards.router, prefix="/flash_card", tags=["FlashCard"])
app.include_router(flash_card_deck.router, prefix="/flash_card_deck", tags=["FlashCardDeck"])

# Allow all origins (for development purposes only)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow any method (GET, POST, etc.)
    allow_headers=["*"],  # Allow any headers
)

# Create the tables
@app.on_event("startup")
async def on_startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

# Root Message
@app.get("/")
async def root():
    return {"message": "Service is walking"}
