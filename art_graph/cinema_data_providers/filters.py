"""Client-side filters for TMDb data.

TMDb API endpoints offer almost no server-side filtering (only response
language and pagination). These filters are applied after fetching results
from the API or cache.
"""

from dataclasses import dataclass, field
from typing import Set

from .tmdb_models import Movie


@dataclass
class MovieFilter:
    """Criteria for filtering movies returned by TMDb.

    All thresholds use >= comparison. An empty allowed_languages set
    disables language filtering (accepts all languages).
    """

    allowed_languages: Set[str] = field(default_factory=lambda: {"en"})
    min_vote_average: float = 0.0
    min_vote_count: int = 0
    min_popularity: float = 0.0
    excluded_genre_ids: Set[int] = field(default_factory=lambda: {99, 10770})

    def accepts(self, movie: Movie) -> bool:
        if (
            self.allowed_languages
            and movie.original_language not in self.allowed_languages
        ):
            return False
        if movie.vote_average < self.min_vote_average:
            return False
        if movie.vote_count < self.min_vote_count:
            return False
        if movie.popularity < self.min_popularity:
            return False
        if self.excluded_genre_ids and movie.genre_ids:
            if self.excluded_genre_ids & set(movie.genre_ids):
                return False
        return True
