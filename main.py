from fastapi import FastAPI

from blog import main as blog_router
from contact import main as contact_router

app = FastAPI()

app.include_router(blog_router.router)
app.include_router(contact_router.router, tags=["Contact"])


@app.get("/", tags=["Home"])
async def home():
    return {"detail": "Hello from Archangel Macsika."}

