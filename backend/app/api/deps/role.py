from fastapi import Depends
from app.core.exceptions import ForbiddenHTTPException
from app.models import UserRole, User
from .auth import get_current_user


def require_roles(*required_roles: UserRole):
    def role_checker(current_user: User = Depends(get_current_user)):
        if not current_user:
            raise ForbiddenHTTPException(msg="Not authenticated")
        try:
            role = UserRole(current_user.role)  # Принудительно в enum
        except ValueError:
            raise ForbiddenHTTPException(msg="Invalid role")

        if role not in required_roles:
            raise ForbiddenHTTPException(msg="Not enough permissions")
        return current_user

    return role_checker


def authorized():
    return require_roles(*UserRole)

def admin_moderator():
    return require_roles(UserRole.moderator, UserRole.admin)

def admin():
    return require_roles(UserRole.admin)