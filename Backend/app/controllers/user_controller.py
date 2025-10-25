"""
User Controller
Uses: rodrigo0000-fastapi-core-controllers, rodrigo0000-fastapi-core-models
Location: venv/lib/python3.x/site-packages/rodrigo0000_fastapi_core_*/
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

# Import from installed PyPI packages
from rodrigo0000_fastapi_core_controllers import BaseController
from rodrigo0000_fastapi_core_models import UserResponse, UserUpdate, PaginatedResponse
from rodrigo0000_fastapi_core_database import get_db
from rodrigo0000_fastapi_core_auth import get_current_user
from rodrigo0000_fastapi_core_services import EmailService

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[UserResponse])
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    List all users with pagination
    Uses BaseController from rodrigo0000-fastapi-core-controllers
    """
    # Use BaseController methods from PyPI package
    users, total = await BaseController.get_paginated(
        db=db,
        model=User,
        page=page,
        page_size=page_size
    )
    
    return PaginatedResponse(
        items=users,
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get user by ID
    Uses BaseController from rodrigo0000-fastapi-core-controllers
    """
    user = await BaseController.get_by_id(db, User, user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Update user information
    Uses BaseController from rodrigo0000-fastapi-core-controllers
    """
    user = await BaseController.update(db, User, user_id, user_data.dict(exclude_unset=True))
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Delete user
    Uses BaseController from rodrigo0000-fastapi-core-controllers
    """
    success = await BaseController.delete(db, User, user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User deleted successfully"}


@router.post("/{user_id}/send-welcome-email")
async def send_welcome_email(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Send welcome email to user
    Uses EmailService from rodrigo0000-fastapi-core-services
    """
    user = await BaseController.get_by_id(db, User, user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Use EmailService from PyPI package
    success = await EmailService.send_welcome_email(user.email, user.full_name or "User")
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send email")
    
    return {"message": "Welcome email sent successfully"}
