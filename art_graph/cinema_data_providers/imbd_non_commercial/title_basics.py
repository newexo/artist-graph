from pydantic import BaseModel
from typing import List, Optional


class TitleBasics(BaseModel):
    tconst: str
    titleType: str
    primaryTitle: str
    originalTitle: str
    isAdult: bool
    startYear: Optional[int] = None
    endYear: Optional[Optional[int]] = None
    runtimeMinutes: Optional[int] = None
    genres: Optional[List[str]] = None
