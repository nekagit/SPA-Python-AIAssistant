from typing import List

from database import database, models
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# GET: Retrieve all flash_card
@router.get("/", response_model=List[models.FlashCard])
async def get_flash_card(db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.FlashCardModel))
    flash_card = result.scalars().all()
    return flash_card

# GET: Retrieve a single flash_card by ID
@router.get("/{flash_card_id}", response_model=models.FlashCard)
async def get_flash_card(flash_card_id: int, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.FlashCardModel).filter(models.FlashCardModel.id == flash_card_id))
    flash_card = result.scalar_one_or_none()
    if flash_card is None:
        raise HTTPException(status_code=404, detail="flash_card not found")
    return flash_card

# POST: Create a new flash_card
@router.post("/", response_model=models.FlashCard)
async def create_flash_card(flash_card: models.FlashCard, db: AsyncSession = Depends(database.get_db)):
    db_flash_card = models.FlashCardModel(**flash_card.model_dump(exclude_unset=True))
    db.add(db_flash_card)
    await db.commit()
    await db.refresh(db_flash_card)
    return db_flash_card

@router.put("/{flash_card_id}", response_model=models.FlashCardUpdate)
async def update_flash_card(flash_card_id: int, updated_flash_card: models.FlashCardUpdate, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.FlashCardModel).filter(models.FlashCardModel.id == flash_card_id))
    db_flash_card = result.scalar_one_or_none()
    if db_flash_card is None:
        raise HTTPException(status_code=404, detail="flash_card not found")

    for key, value in updated_flash_card.model_dump(exclude_unset=True).items():
        setattr(db_flash_card, key, value)
    await db.commit()
    await db.refresh(db_flash_card)
    return db_flash_card

@router.patch("/{flash_card_id}", response_model=models.FlashCardUpdate)
async def patch_flash_card(flash_card_id: int, flash_card_data: models.FlashCardUpdate, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.FlashCardModel).filter(models.FlashCardModel.id == flash_card_id))
    db_flash_card = result.scalar_one_or_none()
    if db_flash_card is None:
        raise HTTPException(status_code=404, detail="flash_card not found")

    for key, value in flash_card_data.model_dump(exclude_unset=True).FlashCard():
        setattr(db_flash_card, key, value)
    await db.commit()
    await db.refresh(db_flash_card)
    return db_flash_card

# DELETE: Delete an flash_card by ID
@router.delete("/{flash_card_id}")
async def delete_flash_card(flash_card_id: int, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.FlashCardModel).filter(models.FlashCardModel.id == flash_card_id))
    db_flash_card = result.scalar_one_or_none()
    if db_flash_card is None:
        raise HTTPException(status_code=404, detail="flash_card not found")
    
    await db.delete(db_flash_card)
    await db.commit()
    return {"detail": f"flash_card {flash_card_id} deleted"}
