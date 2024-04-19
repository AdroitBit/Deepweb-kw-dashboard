from enum import Enum
from typing import Dict, List
from pydantic import BaseModel
class DeepWebInfo(BaseModel):
    keyword: str
    url: str

class DeepWebSuggest(BaseModel):
    url: str

class PushKeyword(BaseModel):
    keyword: str

class ServerHealth(BaseModel):
    cpu_percent: float
    memory_percent: float