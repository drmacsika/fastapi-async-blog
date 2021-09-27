
from fastapi import Depends, FastAPI

# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from tortoise.contrib.fastapi import register_tortoise
from blog import main as blog_router

app = FastAPI()

app.include_router(blog_router.router, tags=["blog"])






@app.get("/", tags=["home"])
async def home():
    return {"Hello": "World"}

# register_tortoise(
#     app,
#     db_url="sqlite://db.sqlite3",
#     modules={'models': ["blog.models", "accounts.models"]},
#     generate_schemas=True,
#     add_exception_handlers=True
# )
