from sqlalchemy import select
from fastapi import Depends, APIRouter, HTTPException
from typing import List
from database import models
from database import database
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# GET: Retrieve all user
@router.get("/", response_model=List[models.User])
async def get_user(db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.UserModel))
    user = result.scalars().all()
    return user

# GET: Retrieve a single user by ID
@router.get("/{user_id}", response_model=models.User)
async def get_user(user_id: int, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.UserModel).filter(models.UserModel.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return user

# POST: Create a new user
@router.post("/", response_model=models.User)
async def create_user(user: models.User, db: AsyncSession = Depends(database.get_db)):
    db_user = models.UserModel(**user.model_dump(exclude_unset=True))
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.put("/{user_id}", response_model=models.UserUpdate)
async def update_user(user_id: int, updated_user: models.UserUpdate, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.UserModel).filter(models.UserModel.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")

    for key, value in updated_user.model_dump(exclude_unset=True).User():
        setattr(db_user, key, value)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.patch("/{user_id}", response_model=models.UserUpdate)
async def patch_user(user_id: int, user_data: models.UserUpdate, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.UserModel).filter(models.UserModel.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")

    for key, value in user_data.model_dump(exclude_unset=True).User():
        setattr(db_user, key, value)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# DELETE: Delete an user by ID
@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.UserModel).filter(models.UserModel.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    
    await db.delete(db_user)
    await db.commit()
    return {"detail": f"user {user_id} deleted"}
