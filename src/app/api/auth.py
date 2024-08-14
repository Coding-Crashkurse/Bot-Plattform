from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import get_db
from app.core.security import create_access_token, verify_password
from app.core.config import settings
from datetime import timedelta

router = APIRouter()


@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: schemas.Login,
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_email(db, email=form_data.email)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
