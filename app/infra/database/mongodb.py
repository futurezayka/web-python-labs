from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:password@mongodb:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "mydatabase")

client = AsyncIOMotorClient(MONGO_URI)
database: AsyncIOMotorDatabase = client[MONGO_DB_NAME]