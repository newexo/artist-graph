from pydantic import BaseModel
from typing import Optional


class TitlePrincipals(BaseModel):
    tconst: str
    ordering: int
    nconst: str
    category: str
    job: Optional[str] = None
    characters: Optional[str] = None
