# from fastapi import FastAPI
# from app.database import Base, engine
# from app import models
# from app.routers import users, auth, projects, tasks

# app = FastAPI()

# Base.metadata.create_all(bind=engine)

# app.include_router(users.router)
# app.include_router(auth.router)
# app.include_router(projects.router)
# app.include_router(tasks.router)

# @app.get("/")
# def read_root():
#     return {"message": "FastAPI connected successfully"}


from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.database import Base, engine
from app import models
from app.routers import users, auth, projects, tasks
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


@app.get("/")
def read_root():
    return {"message": "FastAPI connected successfully"}