"""Authentication middleware for FastAPI.

For this demo app, Better Auth manages sessions on the frontend.
The backend validates that an auth header is present and trusts
the user_id from the URL path (which comes from the authenticated session).

In production, you would validate the session token against Better Auth's
session store or use a proper JWT-based approach.
"""

from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from ..config import settings

security = HTTPBearer()


class TokenPayload:
    """Token payload containing user info."""

    def __init__(self, user_id: str, email: str = "", exp: int = 0):
        self.user_id = user_id
        self.email = email
        self.exp = exp


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> TokenPayload:
    """
    Verify that an authorization header is present.

    For this demo, we trust the session token from Better Auth.
    The actual user_id comes from the URL path parameter.
    """
    token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    # For demo purposes, we accept any non-empty token
    # The user_id will come from the URL path and be validated in verify_user_access
    # In production, you would validate this token against Better Auth's session store

    if settings.DEBUG:
        print(f"[AUTH] Received session token (length: {len(token)})")

    # Return a placeholder - actual user_id comes from URL
    return TokenPayload(user_id="from_url", email="", exp=0)


def get_current_user(token: TokenPayload = Depends(verify_token)) -> str:
    """Returns the current user's ID."""
    return token.user_id


def verify_user_access(user_id_param: str, token: TokenPayload) -> None:
    """
    Verify that the request is authenticated.

    For this demo, we trust that the frontend sends the correct user_id
    from the authenticated Better Auth session. The presence of a valid
    session token (checked in verify_token) is sufficient.

    In production, you would verify the token contains the same user_id.
    """
    # For demo: just ensure token exists (already checked in verify_token)
    # The user_id_param from URL is trusted as it comes from the auth session
    if not user_id_param:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID is required",
        )
