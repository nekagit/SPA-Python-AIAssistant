from sqlalchemy import select
from fastapi import Depends, APIRouter, HTTPException
from typing import List
from database import models
from database import database
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
not_found_error_message = 'crew not found'
# GET: Retrieve all crew
@router.get("/", response_model=List[models.Crew])
async def get_crew(db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.CrewModel))
    crew = result.scalars().all()
    return crew

# GET: Retrieve a single crew by ID
@router.get("/{crew_id}", response_model=models.Crew)
async def get_crew(crew_id: int, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.CrewModel).filter(models.CrewModel.id == crew_id))
    crew = result.scalar_one_or_none()
    if crew is None:
        raise HTTPException(status_code=404, detail=not_found_error_message)
    return crew

# POST: Create a new crew
@router.post("/", response_model=models.Crew)
async def create_crew(crew: models.Crew, db: AsyncSession = Depends(database.get_db)):
    db_crew = models.CrewModel(**crew.model_dump(exclude_unset=True))
    db.add(db_crew)
    await db.commit()
    await db.refresh(db_crew)
    return db_crew

@router.put("/{crew_id}", response_model=models.CrewUpdate)
async def update_crew(crew_id: int, updated_crew: models.CrewUpdate, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.CrewModel).filter(models.CrewModel.id == crew_id))
    db_crew = result.scalar_one_or_none()
    if db_crew is None:
        raise HTTPException(status_code=404, detail=not_found_error_message)

    for key, value in updated_crew.model_dump(exclude_unset=True).crew():
        setattr(db_crew, key, value)
    await db.commit()
    await db.refresh(db_crew)
    return db_crew

@router.patch("/{crew_id}", response_model=models.CrewUpdate)
async def patch_crew(crew_id: int, crew_data: models.CrewUpdate, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.CrewModel).filter(models.CrewModel.id == crew_id))
    db_crew = result.scalar_one_or_none()
    if db_crew is None:
        raise HTTPException(status_code=404, detail=not_found_error_message)

    for key, value in crew_data.model_dump(exclude_unset=True).crew():
        setattr(db_crew, key, value)
    await db.commit()
    await db.refresh(db_crew)
    return db_crew

# DELETE: Delete an crew by ID
@router.delete("/{crew_id}")
async def delete_crew(crew_id: int, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.CrewModel).filter(models.CrewModel.id == crew_id))
    db_crew = result.scalar_one_or_none()
    if db_crew is None:
        raise HTTPException(status_code=404, detail=not_found_error_message)
    
    await db.delete(db_crew)
    await db.commit()
    return {"detail": f"crew {crew_id} deleted"}
