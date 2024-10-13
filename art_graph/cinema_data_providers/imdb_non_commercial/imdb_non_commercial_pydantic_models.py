from pydantic import BaseModel
from typing import List, Optional


class NameBasics(BaseModel):
    nconst: str
    primaryName: str
    birthYear: Optional[int] = None
    deathYear: Optional[int] = None
    primaryProfession: Optional[List[str]] = None
    knownForTitles: Optional[List[str]] = None


class TitleAkas(BaseModel):
    titleId: str
    ordering: int
    title: str
    region: Optional[str] = None
    language: Optional[str] = None
    types: Optional[List[str]] = None
    attributes: Optional[List[str]] = None
    isOriginalTitle: bool


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


class TitleCrew(BaseModel):
    tconst: str
    directors: Optional[List[str]] = None
    writers: Optional[List[str]] = None


class TitleEpisode(BaseModel):
    tconst: str
    parentTconst: str
    seasonNumber: Optional[int] = None
    episodeNumber: Optional[int] = None


class TitlePrincipals(BaseModel):
    tconst: str
    ordering: int
    nconst: str
    category: str
    job: Optional[str] = None
    characters: Optional[str] = None


class TitleRatings(BaseModel):
    tconst: str
    averageRating: float
    numVotes: int
