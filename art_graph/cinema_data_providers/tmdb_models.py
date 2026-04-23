from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from .tmdb.config import DEFAULT_TMDB_IMAGE_BASE, DEFAULT_TMDB_BACKDROP_BASE


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
    adult: bool = False
    backdrop_path: Optional[str] = None
    genre_ids: Optional[List[int]] = Field(default_factory=list)
    id: int
    original_language: str = "en"
    original_title: str = ""
    overview: str = ""
    popularity: float = 0.0
    poster_path: Optional[str] = None
    release_date: Optional[date] = None
    title: str = ""
    name: Optional[str] = None
    video: bool = False
    vote_average: float = 0.0
    vote_count: int = 0
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

    @model_validator(mode="after")
    def _default_title_and_original_title(self):
        if not self.title and self.name:
            self.title = self.name
        if not self.original_title:
            self.original_title = self.title
        return self

    @property
    def year(self) -> Optional[str]:
        return str(self.release_date.year) if self.release_date else None

    @property
    def poster_url(self) -> Optional[str]:
        return (
            f"{DEFAULT_TMDB_IMAGE_BASE}{self.poster_path}" if self.poster_path else None
        )

    @property
    def backdrop_url(self) -> Optional[str]:
        return (
            f"{DEFAULT_TMDB_BACKDROP_BASE}{self.backdrop_path}"
            if self.backdrop_path
            else None
        )


class Person(BaseModel):
    adult: bool = False
    gender: int = 0
    id: int
    known_for_department: str = "Acting"
    name: str
    original_name: str = ""
    popularity: float = 0.0
    profile_path: Optional[str] = None
    known_for: List[Movie] = Field(default_factory=list)

    @model_validator(mode="after")
    def _default_original_name(self):
        if not self.original_name:
            self.original_name = self.name
        return self

    @property
    def profile_url(self) -> Optional[str]:
        return (
            f"{DEFAULT_TMDB_IMAGE_BASE}{self.profile_path}"
            if self.profile_path
            else None
        )


class MovieSearchResults(BaseModel):
    page: int
    results: List[Movie]
    total_pages: int
    total_results: int


class PersonSearchResults(BaseModel):
    page: int
    results: List[Person]
    total_pages: int
    total_results: int


class CastMember(Person):
    """A Person appearing in a movie's cast.

    Matches one entry in /movie/{id}/credits.cast.
    """

    cast_id: Optional[int] = None
    character: Optional[str] = None
    credit_id: Optional[str] = None
    order: Optional[int] = None


class CrewMember(Person):
    """A Person serving on a movie's crew (writer, director, producer, etc.).

    Matches one entry in /movie/{id}/credits.crew.
    """

    credit_id: Optional[str] = None
    department: Optional[str] = None
    job: Optional[str] = None


class MovieCreditRole(Movie):
    """A Movie in which a person acted.

    Matches one entry in /person/{id}/movie_credits.cast.
    """

    character: Optional[str] = None
    credit_id: Optional[str] = None
    order: Optional[int] = None


class MovieCrewRole(Movie):
    """A Movie in which a person served on the crew.

    Matches one entry in /person/{id}/movie_credits.crew.
    """

    credit_id: Optional[str] = None
    department: Optional[str] = None
    job: Optional[str] = None


class MovieCredits(BaseModel):
    """Response shape for /movie/{id}/credits."""

    id: int
    cast: List[CastMember] = Field(default_factory=list)
    crew: List[CrewMember] = Field(default_factory=list)


class PersonMovieCredits(BaseModel):
    """Response shape for /person/{id}/movie_credits."""

    id: int
    cast: List[MovieCreditRole] = Field(default_factory=list)
    crew: List[MovieCrewRole] = Field(default_factory=list)
