from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class BelongsToCollection(BaseModel):
    id: int
    name: str
    poster_path: Optional[str]
    backdrop_path: Optional[str]


class Genre(BaseModel):
    id: int
    name: str


class ProductionCompany(BaseModel):
    id: int
    logo_path: Optional[str]
    name: str
    origin_country: str


class ProductionCountry(BaseModel):
    iso_3166_1: str
    name: str


class SpokenLanguage(BaseModel):
    english_name: str
    iso_639_1: str
    name: str


class Movie(BaseModel):
    adult: bool
    backdrop_path: Optional[str]
    genre_ids: Optional[List[int]] = Field(
        default_factory=list
    )  # Make genre_ids optional
    id: int
    original_language: str
    original_title: str
    overview: str
    popularity: float
    poster_path: Optional[str]
    release_date: Optional[date]
    title: str
    video: bool
    vote_average: float
    vote_count: int
    belongs_to_collection: Optional[BelongsToCollection] = None
    budget: Optional[int] = None
    genres: Optional[List[Genre]] = Field(default_factory=list)
    homepage: Optional[str] = None
    imdb_id: Optional[str] = None
    production_companies: Optional[List[ProductionCompany]] = Field(
        default_factory=list
    )
    production_countries: Optional[List[ProductionCountry]] = Field(
        default_factory=list
    )
    revenue: Optional[int] = None
    runtime: Optional[int] = None
    spoken_languages: Optional[List[SpokenLanguage]] = Field(default_factory=list)
    status: Optional[str] = None
    tagline: Optional[str] = None
    media_type: Optional[str] = None

    @field_validator("release_date", mode="before")
    def check_release_date(cls, v):
        if v == "":
            return None
        return v


class Actor(BaseModel):
    adult: bool
    gender: int
    id: int
    known_for_department: str
    name: str
    original_name: str
    popularity: float
    profile_path: Optional[str] = None
    known_for: List[Movie]


class MovieSearchResults(BaseModel):
    page: int
    results: List[Movie]
    total_pages: int
    total_results: int


class ActorSearchResults(BaseModel):
    page: int
    results: List[Actor]
    total_pages: int
    total_results: int
