from fastapi import FastAPI

from accounts import main as account_router
from blog import main as blog_router
from contact import main as contact_router

app = FastAPI()

app.include_router(blog_router.router)
app.include_router(contact_router.router, tags=["Contact"])
app.include_router(account_router.router, tags=["Users"])


@app.get("/", tags=["Home"])
async def home():
    return {"detail": "Hello from Archangel Macsika."}

