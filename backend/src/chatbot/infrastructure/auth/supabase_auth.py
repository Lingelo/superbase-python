"""Supabase authentication middleware."""
import jwt
from typing import Optional
from uuid import UUID
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.chatbot.infrastructure.config import settings
from src.chatbot.domain.entities.user import User


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> User:
    """
    Extract and validate JWT token from Authorization header.

    Args:
        credentials: HTTP Bearer token from request header

    Returns:
        User entity with id and email

    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials

    try:
        # Decode JWT token using Supabase JWT secret
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            audience="authenticated",
        )

        # Extract user information from token
        user_id = payload.get("sub")
        email = payload.get("email")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication token: missing user ID"
            )

        return User(id=UUID(user_id), email=email or "")

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Authentication token has expired"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authentication token: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid user ID format: {str(e)}"
        )
