from typing import Dict, List
from pydantic import BaseModel
class DeepWebInfo(BaseModel):
    keyword_and_url: Dict[str, List[str]]