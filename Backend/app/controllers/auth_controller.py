"""
Authentication Controller
Uses: rodrigo0000-fastapi-core-auth (installed in venv)
Location: venv/lib/python3.x/site-packages/rodrigo0000_fastapi_core_auth/
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Import from installed PyPI packages
from rodrigo0000_fastapi_core_auth import (
    AuthService,
    JWTHandler,
    get_current_user,
    create_access_token,
    create_refresh_token
)
from rodrigo0000_fastapi_core_models import UserLogin, UserCreate, UserResponse, Token
from rodrigo0000_fastapi_core_database import get_db

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    Uses AuthService from rodrigo0000-fastapi-core-auth
    """
    try:
        user = await AuthService.register_user(db, user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login user and return JWT tokens
    Uses AuthService and JWTHandler from rodrigo0000-fastapi-core-auth
    """
    user = await AuthService.authenticate_user(db, credentials.email, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
    refresh_token = create_refresh_token(data={"sub": user.email, "user_id": user.id})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user = Depends(get_current_user)):
    """
    Get current authenticated user
    Uses get_current_user dependency from rodrigo0000-fastapi-core-auth
    """
    return current_user


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str):
    """
    Refresh access token using refresh token
    Uses JWTHandler from rodrigo0000-fastapi-core-auth
    """
    payload = JWTHandler.verify_token(refresh_token)
    
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    access_token = create_access_token(data={"sub": payload["sub"], "user_id": payload["user_id"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
