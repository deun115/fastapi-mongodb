from db.models import Item
from db.db import collection
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError
from fastapi import HTTPException
from main import app


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