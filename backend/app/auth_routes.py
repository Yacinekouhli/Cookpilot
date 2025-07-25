from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import secrets
import os

from app.database import get_db
from app.models import User, EmailVerificationToken
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.utils.email import send_verification_email

router = APIRouter(prefix="/auth", tags=["auth"])

# ------------------------
# SCHEMAS
# ------------------------


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class SignupResponse(BaseModel):
    message: str


class VerifyEmailResponse(BaseModel):
    message: str

# ------------------------
# ENV config
# ------------------------

EMAIL_VERIF_TOKEN_TTL_HOURS = int(os.getenv("EMAIL_VERIF_TOKEN_TTL_HOURS", "24"))

# ------------------------
# ROUTES
# ------------------------

@router.post("/signup", response_model=SignupResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    hashed_pwd = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed_pwd, is_verified=False)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(hours=EMAIL_VERIF_TOKEN_TTL_HOURS)

    verif = EmailVerificationToken(
        token=token,
        user_id=new_user.id,
        expires_at=expires_at,
        used=False
    )
    db.add(verif)
    db.commit()

    send_verification_email(new_user.email, token)

    return {"message": "Utilisateur créé. Vérifiez votre e-mail pour activer votre compte."}


@router.get("/verify-email", response_model=VerifyEmailResponse)
def verify_email(token: str = Query(...), db: Session = Depends(get_db)):
    verif = (
        db.query(EmailVerificationToken)
        .filter(EmailVerificationToken.token == token, EmailVerificationToken.used == False)
        .first()
    )

    if not verif:
        raise HTTPException(status_code=400, detail="Token invalide ou déjà utilisé")

    if verif.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expiré")

    user = db.query(User).filter(User.id == verif.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    user.is_verified = True
    verif.used = True
    db.commit()

    return {"message": "✅ Votre email a bien été vérifié. Vous pouvez maintenant vous connecter."}


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email non vérifié. Veuillez confirmer votre adresse.")

    access_token = create_access_token(data={"sub": user.email})

    return TokenResponse(access_token=access_token)
