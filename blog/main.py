from core.database import Base, engine
from fastapi import APIRouter

from blog import models, schemas

router = APIRouter()
# models.Base.metadata.create_all(engine)


# @app.on_event("startup")
# async def startup():
#     # create db tables
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
        

# async def init_models():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)



@router.get("/blog")
async def blog():
    return {
        "detail": "Post executed successfully"
    }

@router.post("/blog/create")
async def create_post(request: schemas.Post):
    return request
