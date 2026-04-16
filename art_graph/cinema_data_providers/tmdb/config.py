"""Configuration for the TMDb HTTP client.

Credentials and endpoints can be passed explicitly via TMDbConfig, or read
from environment variables via the create_tmdb_config convenience function.
"""

import os
from typing import Optional

DEFAULT_TMDB_BASE_URL = "https://api.themoviedb.org/3"
DEFAULT_TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
DEFAULT_TMDB_BACKDROP_BASE = "https://image.tmdb.org/t/p/w1280"


class TMDbConfig:
    """TMDb configuration with explicit credential injection."""

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        image_base: Optional[str] = None,
        backdrop_base: Optional[str] = None,
        timeout: Optional[float] = None,
    ):
        self.api_key = api_key
        self.base_url = base_url or DEFAULT_TMDB_BASE_URL
        self.image_base = image_base or DEFAULT_TMDB_IMAGE_BASE
        self.backdrop_base = backdrop_base or DEFAULT_TMDB_BACKDROP_BASE
        self.timeout = timeout if timeout is not None else 10.0


def create_tmdb_config(
    base_url: Optional[str] = None,
    image_base: Optional[str] = None,
    backdrop_base: Optional[str] = None,
    timeout: Optional[float] = None,
) -> TMDbConfig:
    """Create a TMDbConfig reading credentials from the environment."""
    return TMDbConfig(
        api_key=os.getenv("TMDB_API_KEY", ""),
        base_url=base_url,
        image_base=image_base,
        backdrop_base=backdrop_base,
        timeout=timeout,
    )


def build_image_url(path: Optional[str], base: str) -> Optional[str]:
    """Prefix a TMDb image path with the given image base URL."""
    return f"{base}{path}" if path else None
