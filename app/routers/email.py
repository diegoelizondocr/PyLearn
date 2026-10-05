from fastapi import APIRouter, Depends

from app.models.schemas import EmailRequest
from app.services.email_service import EmailService

router = APIRouter(prefix="/email", tags=["Email"])


@router.post("")
def send_email(
    email_data: EmailRequest,
    service: EmailService = Depends(EmailService),
) -> dict:
    return service.send_email_new(email_data)
