from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = "mongodb://mongodb:mongodb@localhost:27017"

client = AsyncIOMotorClient(
    MONGO_DETAILS,
    maxPoolSize=100,         # 커넥션 풀 최대 크기 (기본: 100)
    minPoolSize=10,          # 커넥션 풀 최소 크기 (기본: 0)
    serverSelectionTimeoutMS=5000  # 서버 응답 대기 시간 (ms))
)
database = client.my_database
collection = database.my_collection

async def connect_to_mongo():
    print("MongoDB connected")

async def close_mongo_connection():
    client.close()
    print("MongoDB connection closed")
