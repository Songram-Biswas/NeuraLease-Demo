from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_properties():
    return {"message": "Property list endpoint"}