from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_session

from models.user import User, UserCreate, UserRead

from auth import verify_api_key

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/", response_model=UserRead)
def register_user(
    user_data: UserCreate,
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key),
):
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An user with this email already exists.",
        )

    user = User.model_validate(user_data)
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@user_router.get("/", response_model=list[UserRead])
def list_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users
