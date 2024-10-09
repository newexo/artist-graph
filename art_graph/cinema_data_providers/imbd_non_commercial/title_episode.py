from pydantic import BaseModel
from typing import Optional


class TitleEpisode(BaseModel):
    tconst: str
    parentTconst: str
    seasonNumber: Optional[int] = None
    episodeNumber: Optional[int] = None
