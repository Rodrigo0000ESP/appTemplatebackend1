"""
Email Controller
Uses: rodrigo0000-fastapi-core-services (EmailService)
Location: venv/lib/python3.x/site-packages/rodrigo0000_fastapi_core_services/
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Import from installed PyPI packages
from rodrigo0000_fastapi_core_services import EmailService
from rodrigo0000_fastapi_core_auth import get_current_user
from rodrigo0000_fastapi_core_database import get_db
from rodrigo0000_fastapi_core_models import (
    EmailSend,
    EmailTemplate,
    EmailResponse
)

router = APIRouter()


@router.post("/send", response_model=EmailResponse)
async def send_email(
    email_data: EmailSend,
    current_user = Depends(get_current_user)
):
    """
    Send a custom email
    Uses EmailService from rodrigo0000-fastapi-core-services
    """
    try:
        success = await EmailService.send_email(
            to=email_data.to,
            subject=email_data.subject,
            body=email_data.body,
            html=email_data.html
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to send email")
        
        return {"success": True, "message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/welcome/{user_id}")
async def send_welcome_email(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Send welcome email to a user
    Uses EmailService from rodrigo0000-fastapi-core-services
    """
    # Get user from database
    from rodrigo0000_fastapi_core_controllers import BaseController
    from rodrigo0000_fastapi_core_models import User
    
    user = await BaseController.get_by_id(db, User, user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        success = await EmailService.send_welcome_email(
            email=user.email,
            name=user.full_name or "User"
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to send email")
        
        return {"success": True, "message": "Welcome email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/password-reset/{email}")
async def send_password_reset_email(
    email: str,
    db: Session = Depends(get_db)
):
    """
    Send password reset email
    Uses EmailService from rodrigo0000-fastapi-core-services
    """
    # Generate reset token
    from rodrigo0000_fastapi_core_auth import JWTHandler
    import secrets
    
    reset_token = secrets.token_urlsafe(32)
    
    try:
        success = await EmailService.send_password_reset_email(
            email=email,
            reset_token=reset_token
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to send email")
        
        return {"success": True, "message": "Password reset email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/verification/{user_id}")
async def send_verification_email(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Send email verification link
    Uses EmailService from rodrigo0000-fastapi-core-services
    """
    from rodrigo0000_fastapi_core_controllers import BaseController
    from rodrigo0000_fastapi_core_models import User
    import secrets
    
    user = await BaseController.get_by_id(db, User, user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    verification_token = secrets.token_urlsafe(32)
    
    try:
        success = await EmailService.send_verification_email(
            email=user.email,
            verification_token=verification_token
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to send email")
        
        return {"success": True, "message": "Verification email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/template", response_model=EmailResponse)
async def send_template_email(
    template_data: EmailTemplate,
    current_user = Depends(get_current_user)
):
    """
    Send email using a template
    Uses EmailService from rodrigo0000-fastapi-core-services
    """
    try:
        success = await EmailService.send_template_email(
            to=template_data.to,
            template_name=template_data.template_name,
            context=template_data.context
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to send email")
        
        return {"success": True, "message": "Template email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/bulk")
async def send_bulk_email(
    email_data: EmailSend,
    current_user = Depends(get_current_user)
):
    """
    Send bulk emails to multiple recipients
    Uses EmailService from rodrigo0000-fastapi-core-services
    Admin only
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        results = await EmailService.send_bulk_email(
            recipients=email_data.to,
            subject=email_data.subject,
            body=email_data.body,
            html=email_data.html
        )
        
        return {
            "success": True,
            "message": f"Sent {results['sent']} emails, {results['failed']} failed",
            "details": results
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
