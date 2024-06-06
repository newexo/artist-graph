from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class Movie(BaseModel):
    adult: bool
    backdrop_path: str
    genre_ids: List[int]
    id: int
    original_language: str
    original_title: str
    overview: str
    popularity: float
    poster_path: str
    release_date: date
    title: str
    video: bool
    vote_average: float
    vote_count: int


class Actor(BaseModel):
    adult: bool
    gender: int
    id: int
    known_for_department: str
    name: str
    original_name: str
    popularity: float
    profile_path: str
    known_for: List[Movie]


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


class MovieDetails(BaseModel):
    adult: bool
    backdrop_path: str
    belongs_to_collection: Optional[BelongsToCollection]
    budget: int
    genres: List[Genre]
    homepage: Optional[str]
    id: int
    imdb_id: Optional[str]
    original_language: str
    original_title: str
    overview: str
    popularity: float
    poster_path: str
    production_companies: List[ProductionCompany]
    production_countries: List[ProductionCountry]
    release_date: str
    revenue: int
    runtime: int
    spoken_languages: List[SpokenLanguage]
    status: str
    tagline: Optional[str]
    title: str
    video: bool
    vote_average: float
    vote_count: int
