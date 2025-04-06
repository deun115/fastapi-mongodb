from fastapi import FastAPI
from fastapi import HTTPException
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError
from db import connect_to_mongo, close_mongo_connection, collection
from middleware import MongoConnectionPoolLoggerMiddleware
from models import Item

app = FastAPI()
app.add_middleware(MongoConnectionPoolLoggerMiddleware)

@app.on_event("startup")
async def startup_db():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db():
    await close_mongo_connection()

@app.post("/items/")
async def create_item(item: Item):
    try:
        result = await collection.insert_one(item.dict())
        return {"inserted_id": str(result.inserted_id)}
    except ServerSelectionTimeoutError:
        raise HTTPException(status_code=503, detail="MongoDB connection failed.")
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/items/")
async def list_items():
    try:
        items = []
        async for item in collection.find():
            item["_id"] = str(item["_id"])
            items.append(item)
        return items
    except ServerSelectionTimeoutError:
        raise HTTPException(status_code=503, detail="MongoDB connection failed.")
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

