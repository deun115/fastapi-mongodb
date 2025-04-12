from db.models import Item
from db.collections import item_collection
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError
from fastapi import HTTPException, APIRouter

item_router = APIRouter()

@item_router.post("/items/")
async def create_item(item: Item):
    try:
        result = await item_collection.insert_one(item.dict(by_alias=True))
        return {"inserted_id": str(result.inserted_id)}
    except ServerSelectionTimeoutError:
        raise HTTPException(status_code=503, detail="MongoDB connection failed.")
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@item_router.get("/item_list/")
async def list_items():
    try:
        items = []
        async for item in item_collection.find():
            item["_id"] = str(item["_id"])
            items.append(item)
        return items
    except ServerSelectionTimeoutError:
        raise HTTPException(status_code=503, detail="MongoDB connection failed.")
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")