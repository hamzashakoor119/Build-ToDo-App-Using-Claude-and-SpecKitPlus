"""JWT authentication middleware for FastAPI."""

from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from typing import Optional
from ..config import settings

security = HTTPBearer()


class TokenPayload:
    """Decoded JWT token payload."""

    def __init__(self, user_id: str, email: str = "", exp: int = 0):
        self.user_id = user_id
        self.email = email
        self.exp = exp


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> TokenPayload:
    """
    Verify JWT token from Authorization header.
    Returns decoded payload with user_id.
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token, settings.BETTER_AUTH_SECRET, algorithms=["HS256"]
        )

        user_id = payload.get("sub") or payload.get("user_id")
        email = payload.get("email", "")
        exp = payload.get("exp", 0)

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id",
            )

        return TokenPayload(user_id=user_id, email=email, exp=exp)

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {str(e)}",
        )


def get_current_user(token: TokenPayload = Depends(verify_token)) -> str:
    """Returns the current user's ID."""
    return token.user_id


def verify_user_access(user_id_param: str, token: TokenPayload) -> None:
    """
    Verify that the authenticated user matches the user_id in the URL.
    Raises 403 if user is trying to access another user's resources.
    """
    if token.user_id != user_id_param:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own resources",
        )
