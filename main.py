from fastapi import Depends, FastAPI

from blog import main as blog_router
from core.settings import init_models

app = FastAPI()

# @app.on_event("startup")
# async def on_startup():
#     await init_models()

app.include_router(blog_router.router, tags=["blog"])

@app.get("/", tags=["home"])
async def home():
    return {"Hello": "World"}

