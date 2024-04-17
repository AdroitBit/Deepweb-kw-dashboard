from typing import Dict, List
from pydantic import BaseModel
class DeepWebInfo(BaseModel):
    keyword: str
    url: str