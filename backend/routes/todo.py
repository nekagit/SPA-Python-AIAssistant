from sqlalchemy import select
from fastapi import Depends, APIRouter, HTTPException
from typing import List
from database import models
from database import database
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# GET: Retrieve all todo
@router.get("/", response_model=List[models.Todo])
async def get_todo(db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.TodoModel))
    todo = result.scalars().all()
    return todo

# GET: Retrieve a single todo by ID
@router.get("/{todo_id}", response_model=models.Todo)
async def get_todo(todo_id: int, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.TodoModel).filter(models.TodoModel.id == todo_id))
    todo = result.scalar_one_or_none()
    if todo is None:
        raise HTTPException(status_code=404, detail="todo not found")
    return todo

# POST: Create a new todo
@router.post("/", response_model=models.Todo)
async def create_todo(todo: models.Todo, db: AsyncSession = Depends(database.get_db)):
    db_todo = models.TodoModel(**todo.model_dump(exclude_unset=True))
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo

@router.put("/{todo_id}", response_model=models.TodoUpdate)
async def update_todo(todo_id: int, updated_todo: models.TodoUpdate, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.TodoModel).filter(models.TodoModel.id == todo_id))
    db_todo = result.scalar_one_or_none()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="todo not found")

    # Update directly from model_dump() without calling .Todo()
    for key, value in updated_todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)
    
    await db.commit()
    await db.refresh(db_todo)
    return db_todo

@router.patch("/{todo_id}", response_model=models.TodoUpdate)
async def patch_todo(todo_id: int, todo_data: models.TodoUpdate, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.TodoModel).filter(models.TodoModel.id == todo_id))
    db_todo = result.scalar_one_or_none()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="todo not found")

    for key, value in todo_data.model_dump(exclude_unset=True).Todo():
        setattr(db_todo, key, value)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo

# DELETE: Delete an todo by ID
@router.delete("/{todo_id}")
async def delete_todo(todo_id: int, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.TodoModel).filter(models.TodoModel.id == todo_id))
    db_todo = result.scalar_one_or_none()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="todo not found")
    
    await db.delete(db_todo)
    await db.commit()
    return {"detail": f"todo {todo_id} deleted"}
