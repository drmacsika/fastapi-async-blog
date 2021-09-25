from codecs import register

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={'models': ['blog.models']},
    generate_schema=True,
    add_exception_handlers=True
)
