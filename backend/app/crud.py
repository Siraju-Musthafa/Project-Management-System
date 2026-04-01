# from sqlalchemy.orm import Session
# from app import models, schemas
# from app.utils import hash_password


# def get_user_by_email(db, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()

# def create_user(db: Session, user: schemas.UserCreate):
#     db_user = models.User(
#         name=user.name,
#         email=user.email,
#         password=hash_password(user.password),
#         role=user.role
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# def get_users(db: Session):
#     return db.query(models.User).all()


# def create_project(db: Session, project: schemas.ProjectCreate, user_id: int):
#     db_project = models.Project(
#         name=project.name,
#         description=project.description,
#         created_by=user_id
#     )
#     db.add(db_project)
#     db.commit()
#     db.refresh(db_project)
#     return db_project


# def get_projects(db: Session):
#     return db.query(models.Project).all()


# def get_project_by_id(db: Session, project_id: int):
#     return db.query(models.Project).filter(models.Project.id == project_id).first()


# def update_project(db: Session, project_id: int, project: schemas.ProjectUpdate):
#     db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
#     if not db_project:
#         return None

#     db_project.name = project.name
#     db_project.description = project.description

#     db.commit()
#     db.refresh(db_project)
#     return db_project


# def delete_project(db: Session, project_id: int):
#     db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
#     if not db_project:
#         return None

#     db.delete(db_project)
#     db.commit()
#     return db_project


# # Task CRUD FUNCTION


# def create_task(db: Session, task: schemas.TaskCreate):
#     db_task = models.Task(
#         title=task.title,
#         description=task.description,
#         status=task.status,
#         project_id=task.project_id,
#         assigned_to=task.assigned_to,
#         due_date=task.due_date
#     )
#     db.add(db_task)
#     db.commit()
#     db.refresh(db_task)
#     return db_task


# def get_tasks(
#     db: Session,
#     project_id: int | None = None,
#     status: str | None = None,
#     assigned_to: int | None = None
# ):
#     query = db.query(models.Task)

#     if project_id is not None:
#         query = query.filter(models.Task.project_id == project_id)

#     if status is not None:
#         query = query.filter(models.Task.status == status)

#     if assigned_to is not None:
#         query = query.filter(models.Task.assigned_to == assigned_to)

#     return query.all()


# def get_task_by_id(db: Session, task_id: int):
#     return db.query(models.Task).filter(models.Task.id == task_id).first()


# def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
#     db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
#     if not db_task:
#         return None

#     db_task.title = task.title
#     db_task.description = task.description
#     db_task.status = task.status
#     db_task.project_id = task.project_id
#     db_task.assigned_to = task.assigned_to
#     db_task.due_date = task.due_date

#     db.commit()
#     db.refresh(db_task)
#     return db_task


# def update_task_status(db: Session, task_id: int, new_status: str):
#     db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
#     if not db_task:
#         return None

#     db_task.status = new_status
#     db.commit()
#     db.refresh(db_task)
#     return db_task


# def delete_task(db: Session, task_id: int):
#     db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
#     if not db_task:
#         return None

#     db.delete(db_task)
#     db.commit()
#     return db_task



from sqlalchemy.orm import Session
from app import models, schemas
from app.utils import hash_password


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role.value
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_project(db: Session, project: schemas.ProjectCreate, user_id: int):
    db_project = models.Project(
        name=project.name,
        description=project.description,
        created_by=user_id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_projects(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Project).offset(skip).limit(limit).all()


def get_project_by_id(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def update_project(db: Session, project_id: int, project: schemas.ProjectUpdate):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        return None

    db_project.name = project.name
    db_project.description = project.description

    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        return None

    db.delete(db_project)
    db.commit()
    return db_project


# def create_task(db: Session, task: schemas.TaskCreate):
#     db_task = models.Task(
#         title=task.title,
#         description=task.description,
#         status=task.status.value,
#         project_id=task.project_id,
#         assigned_to=task.assigned_to,
#         due_date=task.due_date
#     )
#     db.add(db_task)
#     db.commit()
#     db.refresh(db_task)
#     return db_task


# def get_tasks(
#     db: Session,
#     project_id: int | None = None,
#     status: str | None = None,
#     assigned_to: int | None = None,
#     skip: int = 0,
#     limit: int = 10
# ):
#     query = db.query(models.Task)

#     if project_id is not None:
#         query = query.filter(models.Task.project_id == project_id)

#     if status is not None:
#         query = query.filter(models.Task.status == status)

#     if assigned_to is not None:
#         query = query.filter(models.Task.assigned_to == assigned_to)

#     return query.offset(skip).limit(limit).all()


# def get_task_by_id(db: Session, task_id: int):
#     return db.query(models.Task).filter(models.Task.id == task_id).first()


# def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
#     db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
#     if not db_task:
#         return None

#     db_task.title = task.title
#     db_task.description = task.description
#     db_task.status = task.status.value
#     db_task.project_id = task.project_id
#     db_task.assigned_to = task.assigned_to
#     db_task.due_date = task.due_date

#     db.commit()
#     db.refresh(db_task)
#     return db_task


# def update_task_status(db: Session, task_id: int, new_status: schemas.TaskStatus):
#     db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
#     if not db_task:
#         return None

#     db_task.status = new_status.value
#     db.commit()
#     db.refresh(db_task)
#     return db_task


# def delete_task(db: Session, task_id: int):
#     db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
#     if not db_task:
#         return None

#     db.delete(db_task)
#     db.commit()
#     return db_task

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        status=task.status.value if hasattr(task.status, "value") else task.status,
        project_id=task.project_id,
        assigned_to=task.assigned_to,
        due_date=task.due_date
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(
    db: Session,
    project_id: int | None = None,
    status: str | None = None,
    assigned_to: int | None = None,
    skip: int = 0,
    limit: int = 10
):
    query = db.query(models.Task)

    if project_id is not None:
        query = query.filter(models.Task.project_id == project_id)

    if status is not None:
        query = query.filter(models.Task.status == status)

    if assigned_to is not None:
        query = query.filter(models.Task.assigned_to == assigned_to)

    return query.offset(skip).limit(limit).all()


def count_tasks(
    db: Session,
    project_id: int | None = None,
    status: str | None = None,
    assigned_to: int | None = None
):
    query = db.query(models.Task)

    if project_id is not None:
        query = query.filter(models.Task.project_id == project_id)

    if status is not None:
        query = query.filter(models.Task.status == status)

    if assigned_to is not None:
        query = query.filter(models.Task.assigned_to == assigned_to)

    return query.count()


def get_task_by_id(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        return None

    update_data = task.dict(exclude_unset=True)

    if "status" in update_data and hasattr(update_data["status"], "value"):
        update_data["status"] = update_data["status"].value

    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task


def update_task_status(db: Session, task_id: int, status):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        return None

    db_task.status = status.value if hasattr(status, "value") else status
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        return None

    db.delete(db_task)
    db.commit()
    return db_task