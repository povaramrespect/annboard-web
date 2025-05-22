from fastapi import FastAPI, APIRouter

from .advertisement import router as advertisement
from .auth import router as auth
from .user import router as user
from .category import router as category
from .admin.advertisements import router as admin_ad
from .admin.users import admin_router as admin_user
from .admin.users import moder_router as moder_user
from .admin.categories import router as category_router

routers = [
    advertisement,
    auth,
    user,
    category,
    admin_ad,
    admin_user,
    moder_user,
    category_router,
]

def register_routers(app: FastAPI):
    for router in routers:
        app.include_router(router)
