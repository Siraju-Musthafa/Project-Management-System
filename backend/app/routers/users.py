# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.database import get_db
# from app import schemas, crud
# from app.auth import get_current_user
# from app import models

# router = APIRouter(
#     prefix="/users",
#     tags=["Users"]
# )


# @router.post("/", response_model=schemas.UserResponse)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     existing_user = crud.get_user_by_email(db, user.email)
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     return crud.create_user(db, user)


# @router.get("/", response_model=list[schemas.UserResponse])
# def list_users(
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(get_current_user)
# ):
#     return crud.get_users(db)


# @router.get("/me", response_model=schemas.UserResponse)
# def get_me(current_user: models.User = Depends(get_current_user)):
#     return current_user


from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, crud
from app.auth import get_current_user
from app import models

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=schemas.UserResponse, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_user(db, user)


@router.get("/", response_model=list[schemas.UserResponse])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_users(db, skip=skip, limit=limit)


@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user