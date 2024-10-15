from pydantic import BaseModel, field_validator
from typing import Optional
from imdb.parser.s3 import utils as s3_utils


class NonCommercialIMDbBaseModel(BaseModel):
    class Config:
        from_attributes = True


class NameBasics(NonCommercialIMDbBaseModel):
    nconst: int
    knownForTitles: Optional[str] = None
    primaryName: Optional[str] = None
    primaryProfession: Optional[str] = None
    deathYear: Optional[int] = None
    birthYear: Optional[int] = None

    @field_validator("nconst", mode="before")
    def check_nconst(cls, v):
        try:
            return int(v)
        except ValueError:
            return s3_utils.transf_imdbid(v)

    @field_validator("knownForTitles", mode="before")
    def check_knownForTitles(cls, v):
        if not v:
            return None
        return s3_utils.transf_multi_imdbid(v)


class TitleAkas(NonCommercialIMDbBaseModel):
    titleId: int
    ordering: Optional[int] = None
    attributes: Optional[str] = None
    types: Optional[str] = None
    title: Optional[str] = None
    isOriginalTitle: Optional[bool] = None
    language: Optional[str] = None
    region: Optional[str] = None

    @field_validator("titleId", mode="before")
    def check_titleId(cls, v):
        try:
            return int(v)
        except ValueError:
            return s3_utils.transf_imdbid(v)


class TitleBasics(NonCommercialIMDbBaseModel):
    tconst: int
    primaryTitle: Optional[str] = None
    originalTitle: Optional[str] = None
    titleType: Optional[str] = None
    isAdult: Optional[bool] = None
    startYear: Optional[int] = None
    endYear: Optional[int] = None
    runtimeMinutes: Optional[int] = None
    genres: Optional[str] = None

    @field_validator("titleType", mode="before")
    def check_titleType(cls, v):
        return s3_utils.transf_kind(v)

    @field_validator("tconst", mode="before")
    def check_tconst(cls, v):
        try:
            return int(v)
        except ValueError:
            return s3_utils.transf_imdbid(v)


class TitleCrew(NonCommercialIMDbBaseModel):
    tconst: int
    writers: Optional[str] = None
    directors: Optional[str] = None

    @field_validator("tconst", mode="before")
    def check_tconst(cls, v):
        try:
            return int(v)
        except ValueError:
            return s3_utils.transf_imdbid(v)

    @field_validator("writers", mode="before")
    def check_writers(cls, v):
        return s3_utils.transf_multi_imdbid(v)

    @field_validator("directors", mode="before")
    def check_directors(cls, v):
        return s3_utils.transf_multi_imdbid(v)


class TitleEpisode(NonCommercialIMDbBaseModel):
    tconst: int
    parentTconst: Optional[int] = None
    seasonNumber: Optional[int] = None
    episodeNumber: Optional[int] = None

    @field_validator("tconst", mode="before")
    def check_tconst(cls, v):
        try:
            return int(v)
        except ValueError:
            return s3_utils.transf_imdbid(v)

    @field_validator("parentTconst", mode="before")
    def check_parentTconst(cls, v):
        try:
            return int(v)
        except ValueError:
            return s3_utils.transf_imdbid(v)


class TitlePrincipals(NonCommercialIMDbBaseModel):
    tconst: int
    nconst: int
    ordering: Optional[int] = None
    job: Optional[str] = None
    category: Optional[str] = None
    characters: Optional[str] = None

    @field_validator("tconst", mode="before")
    def check_tconst(cls, v):
        try:
            return int(v)
        except ValueError:
            return s3_utils.transf_imdbid(v)

    @field_validator("nconst", mode="before")
    def check_nconst(cls, v):
        try:
            return int(v)
        except ValueError:
            return s3_utils.transf_imdbid(v)


class TitleRatings(NonCommercialIMDbBaseModel):
    tconst: int
    averageRating: Optional[float] = None
    numVotes: Optional[int] = None

    @field_validator("tconst", mode="before")
    def check_tconst(cls, v):
        try:
            return int(v)
        except ValueError:
            return s3_utils.transf_imdbid(v)
