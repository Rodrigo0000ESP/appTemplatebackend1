"""
Email Controller - Simplified version
Uses: fastapi_core_services (EmailService)
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from fastapi_core_services import EmailService
from fastapi_core_database import get_db, get_current_user
from fastapi_core_models import User

router = APIRouter()


class EmailSend(BaseModel):
    to: EmailStr
    subject: str
    body: str


@router.post("/send")
async def send_email(
    email_data: EmailSend,
    current_user: dict = Depends(get_current_user)
):
    """Send a custom email"""
    try:
        email_service = EmailService()
        success = email_service.send_email(
            to_email=email_data.to,
            subject=email_data.subject,
            body=email_data.body,
            is_html=True
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to send email")
        
        return {
            "success": True,
            "message": "Email sent successfully",
            "to": email_data.to
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/welcome/{user_id}")
async def send_welcome_email(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Send welcome email to a user"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        email_service = EmailService()
        
        # Create welcome email HTML
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2>Welcome to R Firm SaaS, {user.username}! 🎉</h2>
                <p>Thank you for joining us. We're excited to have you on board!</p>
                <p>Your account has been successfully created with the email: <strong>{user.email}</strong></p>
                <p>If you have any questions, feel free to reach out to our support team.</p>
                <br>
                <p>Best regards,<br>The R Firm Team</p>
            </body>
        </html>
        """
        
        success = email_service.send_email(
            to_email=user.email,
            subject="Welcome to R Firm SaaS!",
            body=html_body,
            is_html=True
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to send welcome email")
        
        return {
            "success": True,
            "message": f"Welcome email sent to {user.email}",
            "user_id": user_id
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
