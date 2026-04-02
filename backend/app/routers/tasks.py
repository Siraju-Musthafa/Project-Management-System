from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas, crud, models
from app.auth import get_current_user, require_admin

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post("/", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    project = crud.get_project_by_id(db, task.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if task.assigned_to is not None:
        assigned_user = db.query(models.User).filter(models.User.id == task.assigned_to).first()
        if not assigned_user:
            raise HTTPException(status_code=404, detail="Assigned user not found")

    try:
        return crud.create_task(db, task)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create task")


@router.get("/", response_model=schemas.TaskListResponse)
def list_tasks(
    project_id: int | None = Query(default=None),
    status_filter: schemas.TaskStatus | None = Query(default=None, alias="status"),
    assigned_to: int | None = Query(default=None),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    final_assigned_to = assigned_to

    # Developer should only see their own tasks
    if current_user.role == "developer":
        final_assigned_to = current_user.id

    skip = (page - 1) * size

    total = crud.count_tasks(
        db,
        project_id=project_id,
        status=status_filter.value if status_filter else None,
        assigned_to=final_assigned_to
    )

    tasks = crud.get_tasks(
        db,
        project_id=project_id,
        status=status_filter.value if status_filter else None,
        assigned_to=final_assigned_to,
        skip=skip,
        limit=size
    )

    return {
        "items": tasks,
        "total": total,
        "page": page,
        "size": size
    }


@router.get("/{task_id}", response_model=schemas.TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    task = crud.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Developer can only view own task
    if current_user.role == "developer" and task.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this task")

    return task


@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    task: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    existing_task = crud.get_task_by_id(db, task_id)
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.project_id is not None:
        project = crud.get_project_by_id(db, task.project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

    if task.assigned_to is not None:
        assigned_user = db.query(models.User).filter(models.User.id == task.assigned_to).first()
        if not assigned_user:
            raise HTTPException(status_code=404, detail="Assigned user not found")

    try:
        updated_task = crud.update_task(db, task_id, task)
        if not updated_task:
            raise HTTPException(status_code=404, detail="Task not found")
        return updated_task
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update task")


@router.patch("/{task_id}/status", response_model=schemas.TaskResponse)
def change_task_status(
    task_id: int,
    status_update: schemas.TaskStatusUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    task = crud.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Developer can only update own assigned task
    if current_user.role == "developer" and task.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")

    try:
        updated_task = crud.update_task_status(db, task_id, status_update.status)
        if not updated_task:
            raise HTTPException(status_code=404, detail="Task not found")
        return updated_task
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update task status")


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    existing_task = crud.get_task_by_id(db, task_id)
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    try:
        deleted_task = crud.delete_task(db, task_id)
        if not deleted_task:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": "Task deleted successfully"}
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete task")