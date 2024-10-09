from pydantic import BaseModel
from typing import List, Optional


class TitleAkas(BaseModel):
    titleId: str
    ordering: int
    title: str
    region: Optional[str] = None
    language: Optional[str] = None
    types: Optional[List[str]] = None
    attributes: Optional[List[str]] = None
    isOriginalTitle: bool
