
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()








app.get("/")
async def home():
    return {"Hello": "World"}

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={'models': ["blog.models", "accounts.models"]},
    generate_schemas=True,
    add_exception_handlers=True
)
