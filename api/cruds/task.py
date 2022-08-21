from typing import List, Tuple, Optional

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


import api.models.task as task_model
import api.schemas.task as task_schema


async def create_task(
    db: AsyncSession, task_create: task_schema.TaskCreate
) -> task_model.Task:
    task = task_model.Task(**task_create.dict())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def get_tasks_with_done(db: AsyncSession) -> List[task_schema.Task]:
    result: Result = await(
        db.execute(
            select(
                task_model.Task.id,
                task_model.Task.title,
                task_model.Done.id.isnot(None).label("done")
            ).outerjoin(task_model.Done)
        )
    )
    return result.all()

async def get_task(db: AsyncSession, task_id: int) -> Optional[task_schema.Task]:
    result: Result = await db.execute(
        select(task_model.Task.id).filter(task_model.Task.id == task_id)
    )
    task: Optional[Tuple[task_model.Task]] = result.first()
    return task[0] if task is not None else None
