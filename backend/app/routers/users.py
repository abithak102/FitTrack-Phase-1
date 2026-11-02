
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_

from ..database import get_db
from ..models import User
from ..schemas import (
    UserCreate,
    UserOut,
    Token,
    UserProfileUpdate,
    ChangePassword
)
from ..auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        or_(
            User.username == user_data.username,
            User.email == user_data.email
        )
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )

    new_user = User(
        username=user_data.username,
        email=str(user_data.email),
        hashed_password=hash_password(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        or_(
            User.username == form_data.username,
            User.email == form_data.username
        )
    ).first()

    if not user or not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserOut)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user
# -------------------------
# UPDATE USER PROFILE
# -------------------------

@router.patch("/me", response_model=UserOut)
def update_my_profile(
    profile_data: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_user = db.query(User).filter(
        or_(
            User.username == profile_data.username,
            User.email == str(profile_data.email)
        ),
        User.id != current_user.id
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )

    current_user.username = profile_data.username
    current_user.email = str(profile_data.email)

    db.commit()
    db.refresh(current_user)

    return current_user


# -------------------------
# CHANGE PASSWORD
# -------------------------

@router.patch("/change-password")
def change_my_password(
    password_data: ChangePassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(
        password_data.current_password,
        current_user.hashed_password
    ):
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect"
        )

    if password_data.current_password == password_data.new_password:
        raise HTTPException(
            status_code=400,
            detail="New password must be different from current password"
        )

    current_user.hashed_password = hash_password(
        password_data.new_password
    )

    db.commit()

    return {
        "message": "Password changed successfully"
    }
