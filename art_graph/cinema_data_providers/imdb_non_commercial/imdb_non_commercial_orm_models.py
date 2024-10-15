from pydantic import BaseModel
from typing import Optional


class NameBasics(BaseModel):
    nconst: int
    knownForTitles: Optional[str] = None
    primaryName: Optional[str] = None
    primaryProfession: Optional[str] = None
    s_soundex: Optional[str] = None
    ns_soundex: Optional[str] = None
    deathYear: Optional[int] = None
    sn_soundex: Optional[str] = None
    birthYear: Optional[int] = None

    class Config:
        orm_mode = True


class TitleAkas(BaseModel):
    titleId: int
    ordering: Optional[int] = None
    attributes: Optional[str] = None
    types: Optional[str] = None
    title: Optional[str] = None
    isOriginalTitle: Optional[bool] = None
    language: Optional[str] = None
    t_soundex: Optional[str] = None
    region: Optional[str] = None

    class Config:
        orm_mode = True


class TitleBasics(BaseModel):
    tconst: int
    primaryTitle: Optional[str] = None
    originalTitle: Optional[str] = None
    titleType: Optional[str] = None
    isAdult: Optional[bool] = None
    startYear: Optional[int] = None
    endYear: Optional[int] = None
    runtimeMinutes: Optional[int] = None
    t_soundex: Optional[str] = None
    genres: Optional[str] = None

    class Config:
        orm_mode = True


class TitleCrew(BaseModel):
    tconst: int
    writers: Optional[str] = None
    directors: Optional[str] = None

    class Config:
        orm_mode = True


class TitleEpisode(BaseModel):
    tconst: int
    parentTconst: Optional[int] = None
    seasonNumber: Optional[int] = None
    episodeNumber: Optional[int] = None

    class Config:
        orm_mode = True


class TitlePrincipals(BaseModel):
    tconst: int
    nconst: int
    ordering: Optional[int] = None
    job: Optional[str] = None
    category: Optional[str] = None
    characters: Optional[str] = None

    class Config:
        orm_mode = True


class TitleRatings(BaseModel):
    tconst: int
    averageRating: Optional[float] = None
    numVotes: Optional[int] = None

    class Config:
        orm_mode = True
