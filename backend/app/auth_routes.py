from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import User
from app.auth import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


# Pydantic schema pour la connexion
class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")

    access_token = create_access_token(data={"sub": user.email})

    return TokenResponse(access_token=access_token)
