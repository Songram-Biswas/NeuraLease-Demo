from fastapi import APIRouter
from app.api.v1.endpoints import auth, properties

api_router = APIRouter()

# Authentication রাউটার যোগ করা
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# Properties (Analyze Lease) রাউটার যোগ করা
api_router.include_router(properties.router, prefix="/properties", tags=["Properties"])