# from pydantic import BaseModel, EmailStr
# from typing import Optional
# from datetime import date



# class UserCreate(BaseModel):
#     name: str
#     email: EmailStr
#     password: str
#     role: str


# class UserResponse(BaseModel):
#     id: int
#     name: str
#     email: EmailStr
#     role: str

#     class Config:
#         from_attributes = True


# class LoginRequest(BaseModel):
#     email: EmailStr
#     password: str


# class Token(BaseModel):
#     access_token: str
#     token_type: str




# class ProjectCreate(BaseModel):
#     name: str
#     description: Optional[str] = None


# class ProjectUpdate(BaseModel):
#     name: str
#     description: Optional[str] = None


# class ProjectResponse(BaseModel):
#     id: int
#     name: str
#     description: Optional[str]
#     created_by: int

#     class Config:
#         from_attributes = True



# class TaskCreate(BaseModel):
#     title: str
#     description: Optional[str] = None
#     status: Optional[str] = "pending"
#     project_id: int
#     assigned_to: int
#     due_date: Optional[date] = None


# class TaskUpdate(BaseModel):
#     title: str
#     description: Optional[str] = None
#     status: str
#     project_id: int
#     assigned_to: int
#     due_date: Optional[date] = None


# class TaskStatusUpdate(BaseModel):
#     status: str


# class TaskResponse(BaseModel):
#     id: int
#     title: str
#     description: Optional[str]
#     status: str
#     project_id: int
#     assigned_to: int
#     due_date: Optional[date]

#     class Config:
#         from_attributes = True        




from pydantic import BaseModel, EmailStr, Field
from typing import Optional,List
from datetime import date
from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    developer = "developer"


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"
    blocked = "blocked"


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    role: UserRole


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    description: Optional[str] = Field(None, max_length=500)


class ProjectUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    description: Optional[str] = Field(None, max_length=500)


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_by: int

    class Config:
        from_attributes = True


# class TaskCreate(BaseModel):
#     title: str = Field(..., min_length=2, max_length=150)
#     description: Optional[str] = Field(None, max_length=1000)
#     status: TaskStatus = TaskStatus.pending
#     project_id: int
#     assigned_to: int
#     due_date: Optional[date] = None


# class TaskUpdate(BaseModel):
#     title: str = Field(..., min_length=2, max_length=150)
#     description: Optional[str] = Field(None, max_length=1000)
#     status: TaskStatus
#     project_id: int
#     assigned_to: int
#     due_date: Optional[date] = None


# class TaskStatusUpdate(BaseModel):
#     status: TaskStatus


# class TaskResponse(BaseModel):
#     id: int
#     title: str
#     description: Optional[str]
#     status: TaskStatus
#     project_id: int
#     assigned_to: int
#     due_date: Optional[date]

#     class Config:
#         from_attributes = True

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.todo
    project_id: int
    assigned_to: Optional[int] = None
    due_date: Optional[date] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    project_id: Optional[int] = None
    assigned_to: Optional[int] = None
    due_date: Optional[date] = None


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    project_id: int
    assigned_to: Optional[int] = None
    due_date: Optional[date] = None

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    items: List[TaskResponse]
    total: int
    page: int
    size: int