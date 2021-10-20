from accounts.auth_endpoints import router as auth_router
from accounts.endpoints import router as accounts_router
from blog.endpoints import router as blog_router
from contact.endpoints import router as contact_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(blog_router.router)
router.include_router(contact_router.router, tags=["Contact"])
router.include_router(accounts_router.router, tags=["Users"])
router.include_router(auth_router.router, tags=["Users Auth"])


@router.get("/", tags=["Home"])
async def home():
    return {"detail": "Hello from Archangel Macsika."}

