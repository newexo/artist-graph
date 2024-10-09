from pydantic import BaseModel
from typing import List, Optional


class NameBasics(BaseModel):
    nconst: str
    primaryName: str
    birthYear: Optional[int] = None
    deathYear: Optional[int] = None
    primaryProfession: Optional[List[str]] = None
    knownForTitles: Optional[List[str]] = None
