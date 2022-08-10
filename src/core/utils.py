from typing import Any

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from src.custom_lib.functions import get_current_active_superuser, send_test_email
from src.user.models import User
from src.user.schemas import Message
from .celery import celery_app

router = APIRouter()


@router.post("/test-celery/", response_model=Message, status_code=201)
def test_celery(
        msg: Message,
        current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Test Celery worker.
    """
    celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}


@router.post("/test-email/", response_model=Message, status_code=201)
def test_email(
        email_to: EmailStr,
        current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}
