from pydantic import BaseModel
from typing import List, Optional


class TitleCrew(BaseModel):
    tconst: str
    directors: Optional[List[str]] = None
    writers: Optional[List[str]] = None
