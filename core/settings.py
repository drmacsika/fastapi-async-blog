from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = 'fastapi-secure-&ixxyzs#f+ycdhfwct8d8)b!c*agg3%0n-b_8ywd2rr@eiw-bo'

    
TORTOISE_ORM = {
        "connections": {
            "default": "sqlite://./db.sqlite3"
            },
        "apps": {
            "models": {
                "models": ["..blog.models", "..accounts.models", "aerich.models"],
                "default_connection": "default",
            },
        }
    }
