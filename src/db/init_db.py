from sqlalchemy.orm import Session

from src.core.config import settings
from src.user import schemas
from src.user.models import User
from src.user.repo.user import get_user_by_email, get_user_by_username
from src.core.security import get_hash_password
from . import base
from .session import engine


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    base.Base.metadata.create_all(bind=engine)

    username_test = get_user_by_username(db, username=settings.FIRST_SUPERUSER_USERNAME)
    email_test = get_user_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    if not username_test and not email_test:
        request = schemas.UserBase(
            username=settings.FIRST_SUPERUSER_USERNAME,
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=get_hash_password(settings.FIRST_SUPERUSER_PASSWORD),
            is_active=True,
            is_superuser=True,
        )
        print("Saving superuser")
        user = User(
            username=request.username,
            email=request.email,
            password=request.password,
            is_active=request.is_active,
            is_superuser=request.is_superuser,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
