from db.models import ProgressRequestObj
from utils.process import execute_progress, save_execute_result


def progress_in_background(progress: ProgressRequestObj):
    execute_res = execute_progress(progress)

    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop()
    loop.run_until_complete(save_execute_result(execute_res))
