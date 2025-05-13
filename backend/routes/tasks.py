from typing import List

from database import database, models
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# GET: Retrieve all task
@router.get("/", response_model=List[models.Task])
async def get_task(db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.TaskModel))
    task = result.scalars().all()
    return task

# GET: Retrieve a single task by ID
@router.get("/{task_id}", response_model=models.Task)
async def get_task(task_id: int, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.TaskModel).filter(models.TaskModel.id == task_id))
    task = result.scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    return task

# POST: Create a new task
@router.post("/", response_model=models.Task)
async def create_task(task: models.Task, db: AsyncSession = Depends(database.get_db)):
    db_task = models.TaskModel(**task.model_dump(exclude_unset=True))
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

@router.put("/{task_id}", response_model=models.TaskUpdate)
async def update_task(task_id: int, updated_task: models.TaskUpdate, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.TaskModel).filter(models.TaskModel.id == task_id))
    db_task = result.scalar_one_or_none()
    if db_task is None:
        raise HTTPException(status_code=404, detail="task not found")

    for key, value in updated_task.model_dump(exclude_unset=True).Task():
        setattr(db_task, key, value)
    await db.commit()
    await db.refresh(db_task)
    return db_task

@router.patch("/{task_id}", response_model=models.TaskUpdate)
async def patch_task(task_id: int, task_data: models.TaskUpdate, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.TaskModel).filter(models.TaskModel.id == task_id))
    db_task = result.scalar_one_or_none()
    if db_task is None:
        raise HTTPException(status_code=404, detail="task not found")

    for key, value in task_data.model_dump(exclude_unset=True).Task():
        setattr(db_task, key, value)
    await db.commit()
    await db.refresh(db_task)
    return db_task

# DELETE: Delete an task by ID
@router.delete("/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.TaskModel).filter(models.TaskModel.id == task_id))
    db_task = result.scalar_one_or_none()
    if db_task is None:
        raise HTTPException(status_code=404, detail="task not found")
    
    await db.delete(db_task)
    await db.commit()
    return {"detail": f"task {task_id} deleted"}
