"""
Plan Controller - Simplified version
Uses: fastapi_core_services (PlanService)
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from fastapi_core_services import PlanService
from fastapi_core_database import get_db, get_current_user

router = APIRouter()


class PlanResponse(BaseModel):
    name: str
    description: str
    price: float


@router.get("/")
async def list_plans():
    """List all available plans"""
    return {
        "plans": [
            {"name": "Free", "description": "Free tier", "price": 0.0},
            {"name": "Pro", "description": "Professional tier", "price": 29.99},
            {"name": "Enterprise", "description": "Enterprise tier", "price": 99.99}
        ]
    }


@router.get("/{plan_id}")
async def get_plan(plan_id: str):
    """Get plan details"""
    return {
        "plan_id": plan_id,
        "message": "Plan details - PlanService integration needed"
    }


@router.post("/subscribe/{plan_id}")
async def subscribe_to_plan(
    plan_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Subscribe to a plan"""
    return {
        "message": f"User {current_user['username']} subscribed to plan {plan_id}",
        "plan_id": plan_id,
        "user_id": current_user["id"]
    }


@router.get("/user/current")
async def get_current_user_plan(
    current_user: dict = Depends(get_current_user)
):
    """Get current user's plan"""
    return {
        "user_id": current_user["id"],
        "plan": "Free",
        "message": "Current plan - PlanService integration needed"
    }
