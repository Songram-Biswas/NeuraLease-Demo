# from fastapi import APIRouter, Depends, HTTPException, status
# from app.core.security import create_access_token, hash_password, verify_password
# from app.models.schemas.auth import LoginRequest, TokenResponse
# from app.db.session import get_db

# router = APIRouter()

# @router.post("/login", response_model=TokenResponse)
# async def login(payload: LoginRequest, db = Depends(get_db)):
#     user = await db.users.find_one({"email": payload.email})
#     if not user or not verify_password(payload.password, user["hashed_password"]):
#         raise HTTPException(status_code=401, detail="Incorrect email or password")
    
#     access_token = create_access_token(subject=str(user["_id"]))
#     return {"access_token": access_token, "token_type": "bearer"}
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas.auth import LoginRequest, TokenResponse
from app.models.schemas.user import UserCreate, UserRead
from app.core.security import create_access_token, verify_password
from app.db.session import get_db
from app.services.data_ops import DataOperations

router = APIRouter()

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, db = Depends(get_db)):
    ops = DataOperations(db)
    
    existing_user = await ops.get_user_by_email(payload.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_dict = payload.model_dump()
    user_id = await ops.create_user(user_dict)
    
    return {**user_dict, "id": user_id, "is_active": True}

@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db = Depends(get_db)):
    ops = DataOperations(db)
    user = await ops.get_user_by_email(payload.email)
    
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(subject=str(user["_id"]))
    return {"access_token": token, "token_type": "bearer"}