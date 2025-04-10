from typing import Literal
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str

class ProgressRequestObj(BaseModel):
    name: str = ""
    initial_path: str = ""
    action: Literal["patch", "inverse_color", "rotate", "resize"] = ""


class ProgressCacheModel(BaseModel):
    name: str = ""
    action: Literal["patch", "inverse_color", "rotate", "resize"] = ""
    status: Literal["initial", "in-progress", "completed", "error"] = ""
    url: str = ""