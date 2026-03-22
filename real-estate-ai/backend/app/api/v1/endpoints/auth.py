from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import create_access_token, hash_password, verify_password
from app.models.schemas.auth import LoginRequest, TokenResponse
from app.db.session import get_db

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db = Depends(get_db)):
    user = await db.users.find_one({"email": payload.email})
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(subject=str(user["_id"]))
    return {"access_token": access_token, "token_type": "bearer"}