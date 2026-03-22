from typing import Optional, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.domain.user import User
from app.core.security import hash_password

class DataOperations:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def get_user_by_email(self, email: str) -> Optional[dict]:
        return await self.db.users.find_one({"email": email})

    async def create_user(self, user_data: dict) -> str:
        user_data["hashed_password"] = hash_password(user_data.pop("password"))
        result = await self.db.users.insert_one(user_data)
        return str(result.inserted_id)

    async def save_property(self, property_data: dict) -> str:
        result = await self.db.properties.insert_one(property_data)
        return str(result.inserted_id)