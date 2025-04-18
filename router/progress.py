from db.models import ProgressRequestObj
from db.collections import progress_cache_collection
from utils.background import progress_in_background
from pymongo.errors import PyMongoError
from fastapi import APIRouter, HTTPException, status, Response, BackgroundTasks

progress_router = APIRouter()

@progress_router.post("/trigger_process/")
async def create_progress(progress: ProgressRequestObj, background_tasks: BackgroundTasks):
    try:
        existing = await progress_cache_collection.find_one({
            "name": progress.name,
            "status": {"$in": ["in-progress", "completed"]}
        })

        if existing:
            return Response(
                content={"message": f"Progress already exists for this name {progress.name}."},
                status_code=status.HTTP_409_CONFLICT
            )

        init_res = {
            "name": progress.name,
            "status": "in-progress",
            "action": progress.action
        }

        await progress_cache_collection.insert_one(init_res)

        background_tasks.add_task(progress_in_background, progress)

    except PyMongoError as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {str(e)}")
    return Response({"message": "Success to register background progress"})


@progress_router.get("/process_result/{name:str}")
async def get_process_result(name: str):
    progress_res = await progress_cache_collection.find_one({"name": name, "status": "completed"})

    if progress_res is None:
        print("Still processing...")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"message": "Success to get background progress result", "result": progress_res["url"]})