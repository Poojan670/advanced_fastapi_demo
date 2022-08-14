from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.core.config import settings
from src.custom_lib.functions import (
    get_db, get_current_active_user,
    get_current_active_superuser, send_new_account_email
)
from src.user import schemas
from src.user.models import User
from src.user.repo.user import get_user_by_email, get_user_by_username, is_superuser, get_user_by_id
from src.core.security import get_hash_password

router = APIRouter()


@router.post('/', status_code=201)
async def register(request: schemas.UserCreate,
                   db: Session = Depends(get_db)) -> Any:
    """
    Register new user
    """
    user_email = get_user_by_email(db, request.email)
    if user_email:
        raise HTTPException(status_code=400, detail=f"User with this email : {request.email} already exist!")

    user_username = get_user_by_username(db, request.username)
    if user_username:
        raise HTTPException(status_code=400, detail=f"User with this email : {request.username} already exist!")

    user = User(
        username=request.username,
        email=request.email,
        password=get_hash_password(request.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    if settings.EMAILS_ENABLED:
        send_new_account_email(
            email_to=request.email, username=request.username, password=request.password
        )

    return JSONResponse({
        "msg": "Confirmation Email Sent Successfully!"
    })


@router.get("/", status_code=200, response_model=List[schemas.ShowUser])
def list_users(db: Session = Depends(get_db),
               offset: int = 0,
               limit: int = 10,
               current_user: User = Depends(get_current_active_superuser),
               ) -> Any:
    """
    Lists All Users
    """

    return db.query(User).offset(offset).limit(limit).all()


@router.get("/{id}", response_model=schemas.ShowUser)
def get_user(
        id: int,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = get_user_by_id(db, id)
    while user is not None:
        if user == current_user:
            return user
        if not is_superuser(current_user):
            raise HTTPException(
                status_code=400, detail="The user doesn't have enough privileges"
            )
    return JSONResponse({
        "msg": "User not found !"
    })


@router.patch("/{id}")
def update_user(
        id: int,
        request: schemas.UpdateUser,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = get_user_by_id(db, id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )

    if request.username:
        check = get_user_by_username(db, request.username)
        if check:
            raise HTTPException(
                status_code=404,
                detail=f"The user with this username : {request.username} already exists",
            )
        user.username = request.username

    if request.email:
        check = get_user_by_email(db, request.email)
        if check:
            raise HTTPException(
                status_code=404,
                detail=f"The user with this email : {request.email} already exists",
            )
        user.email = request.email

    db.add(user)
    db.commit()

    return JSONResponse({
        "msg": "User Updated Successfully!"
    })


@router.patch("/{id}/change-password", status_code=200)
def change_password(
        id: int,
        request: schemas.ChangePassword,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Change User Password
    """

    user = get_user_by_id(db, id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )

    if request.new_password != request.confirm_password:
        raise HTTPException(
            status_code=400,
            detail=f"Password's don't match",
        )

    user.password = get_hash_password(request.confirm_password)
    db.add(user)
    db.commit()

    return JSONResponse({
        "msg": "Password Changed Successfully !"
    })


@router.delete("/{id}", status_code=404)
def delete_user(
        id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_superuser)
) -> Any:
    """
    Delete a user
    """

    user = get_user_by_id(db, id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )

    if user != current_user and not is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )

    db.delete(user)
    db.commit()
    return JSONResponse({
        "msg": "Deleted User Successfully!"
    })
