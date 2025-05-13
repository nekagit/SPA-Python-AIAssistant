from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import database, models

router = APIRouter()

@router.get("/", response_model=List[models.Deck])
async def get_all_decks(db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.DeckModel))
    decks = result.scalars().unique().all()
    return decks

@router.get("/{deck_id}", response_model=models.Deck)
async def get_deck(deck_id: int, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(
        select(models.DeckModel).filter(models.DeckModel.id == deck_id)
    )
    deck = result.scalar_one_or_none()
    if deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    return deck

@router.post("/", response_model=models.Deck)
async def create_deck(deck: models.DeckCreate, db: AsyncSession = Depends(database.get_db)):
    # Create deck
    db_deck = models.DeckModel(name=deck.name)
    db.add(db_deck)
    await db.flush()
    
    # Add flashcards if provided
    if deck.flashcards:
        for card in deck.flashcards:
            db_card = models.FlashCardModel(
                front=card.front,
                back=card.back,
                deckId=db_deck.id
            )
            db.add(db_card)
    
    await db.commit()
    await db.refresh(db_deck)
    return db_deck

@router.put("/{deck_id}", response_model=models.Deck)
async def update_deck(
    deck_id: int, 
    deck: models.DeckUpdate, 
    db: AsyncSession = Depends(database.get_db)
):
    result = await db.execute(
        select(models.DeckModel).filter(models.DeckModel.id == deck_id)
    )
    db_deck = result.scalar_one_or_none()
    if db_deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")

    if deck.name is not None:
        db_deck.name = deck.name
    
    await db.commit()
    await db.refresh(db_deck)
    return db_deck

@router.delete("/{deck_id}")
async def delete_deck(deck_id: int, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(
        select(models.DeckModel).filter(models.DeckModel.id == deck_id)
    )
    db_deck = result.scalar_one_or_none()
    if db_deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    
    await db.delete(db_deck)
    await db.commit()
    return {"detail": f"Deck {deck_id} deleted"}