from pydantic import BaseModel


class TitleRatings(BaseModel):
    tconst: str
    averageRating: float
    numVotes: int
