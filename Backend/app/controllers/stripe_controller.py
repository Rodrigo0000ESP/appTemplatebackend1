"""
Stripe/Payment Controller
Uses: rodrigo0000-fastapi-core-services (StripeService)
Location: venv/lib/python3.x/site-packages/rodrigo0000_fastapi_core_services/
"""

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional

# Import from installed PyPI packages
from rodrigo0000_fastapi_core_services import StripeService
from rodrigo0000_fastapi_core_auth import get_current_user
from rodrigo0000_fastapi_core_database import get_db
from rodrigo0000_fastapi_core_models import (
    PaymentIntentCreate,
    PaymentIntentResponse,
    SubscriptionCreate,
    SubscriptionResponse,
    WebhookEvent
)

router = APIRouter()


@router.post("/payment-intent", response_model=PaymentIntentResponse)
async def create_payment_intent(
    payment_data: PaymentIntentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Create a Stripe payment intent
    Uses StripeService from rodrigo0000-fastapi-core-services
    """
    try:
        payment_intent = await StripeService.create_payment_intent(
            amount=payment_data.amount,
            currency=payment_data.currency,
            customer_id=current_user.stripe_customer_id,
            metadata=payment_data.metadata
        )
        return payment_intent
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/subscription", response_model=SubscriptionResponse)
async def create_subscription(
    subscription_data: SubscriptionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Create a Stripe subscription
    Uses StripeService from rodrigo0000-fastapi-core-services
    """
    try:
        subscription = await StripeService.create_subscription(
            customer_id=current_user.stripe_customer_id,
            price_id=subscription_data.price_id,
            trial_days=subscription_data.trial_days
        )
        return subscription
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/subscription/{subscription_id}", response_model=SubscriptionResponse)
async def get_subscription(
    subscription_id: str,
    current_user = Depends(get_current_user)
):
    """
    Get subscription details
    Uses StripeService from rodrigo0000-fastapi-core-services
    """
    try:
        subscription = await StripeService.get_subscription(subscription_id)
        return subscription
    except Exception as e:
        raise HTTPException(status_code=404, detail="Subscription not found")


@router.delete("/subscription/{subscription_id}")
async def cancel_subscription(
    subscription_id: str,
    current_user = Depends(get_current_user)
):
    """
    Cancel a subscription
    Uses StripeService from rodrigo0000-fastapi-core-services
    """
    try:
        result = await StripeService.cancel_subscription(subscription_id)
        return {"message": "Subscription cancelled successfully", "subscription": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/customer")
async def create_customer(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Create a Stripe customer for the current user
    Uses StripeService from rodrigo0000-fastapi-core-services
    """
    try:
        customer = await StripeService.create_customer(
            email=current_user.email,
            name=current_user.full_name,
            metadata={"user_id": str(current_user.id)}
        )
        
        # Update user with stripe_customer_id
        current_user.stripe_customer_id = customer.id
        db.commit()
        
        return {"customer_id": customer.id, "message": "Customer created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/webhook")
async def stripe_webhook(
    webhook_event: WebhookEvent,
    stripe_signature: Optional[str] = Header(None)
):
    """
    Handle Stripe webhooks
    Uses StripeService from rodrigo0000-fastapi-core-services
    """
    try:
        event = await StripeService.verify_webhook(
            payload=webhook_event.dict(),
            signature=stripe_signature
        )
        
        # Handle different event types
        if event.type == "payment_intent.succeeded":
            await StripeService.handle_payment_success(event.data)
        elif event.type == "customer.subscription.created":
            await StripeService.handle_subscription_created(event.data)
        elif event.type == "customer.subscription.deleted":
            await StripeService.handle_subscription_cancelled(event.data)
        
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/prices")
async def list_prices():
    """
    List available Stripe prices
    Uses StripeService from rodrigo0000-fastapi-core-services
    """
    try:
        prices = await StripeService.list_prices()
        return {"prices": prices}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
