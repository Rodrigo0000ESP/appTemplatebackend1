"""
Plan Management Controller
Uses: rodrigo0000-fastapi-core-services (PlanService)
Location: venv/lib/python3.x/site-packages/rodrigo0000_fastapi_core_services/
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

# Import from installed PyPI packages
from rodrigo0000_fastapi_core_services import PlanService
from rodrigo0000_fastapi_core_auth import get_current_user
from rodrigo0000_fastapi_core_database import get_db
from rodrigo0000_fastapi_core_models import (
    PlanCreate,
    PlanUpdate,
    PlanResponse,
    PaginatedResponse,
    UserPlanResponse
)

router = APIRouter()


@router.get("/", response_model=List[PlanResponse])
async def list_plans(
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """
    List all available plans
    Uses PlanService from rodrigo0000-fastapi-core-services
    """
    try:
        plans = await PlanService.list_plans(db, active_only=active_only)
        return plans
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{plan_id}", response_model=PlanResponse)
async def get_plan(
    plan_id: int,
    db: Session = Depends(get_db)
):
    """
    Get plan details by ID
    Uses PlanService from rodrigo0000-fastapi-core-services
    """
    plan = await PlanService.get_plan(db, plan_id)
    
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    return plan


@router.post("/", response_model=PlanResponse)
async def create_plan(
    plan_data: PlanCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Create a new plan (admin only)
    Uses PlanService from rodrigo0000-fastapi-core-services
    """
    # Check if user is admin
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        plan = await PlanService.create_plan(db, plan_data)
        return plan
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{plan_id}", response_model=PlanResponse)
async def update_plan(
    plan_id: int,
    plan_data: PlanUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Update plan details (admin only)
    Uses PlanService from rodrigo0000-fastapi-core-services
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        plan = await PlanService.update_plan(db, plan_id, plan_data)
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        return plan
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{plan_id}")
async def delete_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Delete a plan (admin only)
    Uses PlanService from rodrigo0000-fastapi-core-services
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        success = await PlanService.delete_plan(db, plan_id)
        if not success:
            raise HTTPException(status_code=404, detail="Plan not found")
        return {"message": "Plan deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/subscribe/{plan_id}", response_model=UserPlanResponse)
async def subscribe_to_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Subscribe current user to a plan
    Uses PlanService from rodrigo0000-fastapi-core-services
    """
    try:
        user_plan = await PlanService.subscribe_user_to_plan(
            db=db,
            user_id=current_user.id,
            plan_id=plan_id
        )
        return user_plan
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/current", response_model=UserPlanResponse)
async def get_current_user_plan(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get current user's active plan
    Uses PlanService from rodrigo0000-fastapi-core-services
    """
    user_plan = await PlanService.get_user_plan(db, current_user.id)
    
    if not user_plan:
        raise HTTPException(status_code=404, detail="No active plan found")
    
    return user_plan


@router.post("/user/cancel")
async def cancel_user_plan(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Cancel current user's plan subscription
    Uses PlanService from rodrigo0000-fastapi-core-services
    """
    try:
        success = await PlanService.cancel_user_plan(db, current_user.id)
        if not success:
            raise HTTPException(status_code=404, detail="No active plan to cancel")
        return {"message": "Plan cancelled successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/history", response_model=PaginatedResponse[UserPlanResponse])
async def get_user_plan_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Get user's plan subscription history
    Uses PlanService from rodrigo0000-fastapi-core-services
    """
    try:
        history, total = await PlanService.get_user_plan_history(
            db=db,
            user_id=current_user.id,
            page=page,
            page_size=page_size
        )
        
        return PaginatedResponse(
            items=history,
            total=total,
            page=page,
            page_size=page_size,
            pages=(total + page_size - 1) // page_size
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
