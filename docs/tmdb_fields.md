# TMDb Movie Fields Reference

This document describes the fields available on movies returned by the TMDb API
and their typical value ranges, based on empirical observation. This information
is useful for configuring `MovieFilter` when building applications on top of
artist-graph.

## Fields available without extra API calls

These fields are present on every `MovieCreditRole` returned by
`TMDbClient.get_person_movies()`. No additional API call is needed.

### `popularity` (float)

A daily trending score calculated by TMDb. Factors include daily votes, views,
favourites, watchlist additions, release date, total votes, and the previous
day's score. The exact formula is not public.

**Typical ranges** (sampled April 2026):

| Category | Range |
|---|---|
| Current blockbusters / trending | 20 - 100+ |
| Well-known films (Inception, Titanic) | 10 - 35 |
| Recognisable but not trending (Blood Diamond, The Aviator) | 5 - 10 |
| Older or less mainstream (Celebrity, A Dangerous Method) | 2 - 5 |
| Obscure (unreleased, no votes) | 0 - 2 |

**Important**: Popularity is volatile. A film's score changes daily based on
trending activity. It is not a reliable long-term measure of how well-known a
film is. Use `vote_count` for that.

### `vote_average` (float, 0 - 10)

The average user rating on TMDb.

| Category | Typical range |
|---|---|
| Highly acclaimed (Inception, 12 Years a Slave) | 7.5 - 8.5 |
| Well-received (The Great Gatsby, Blood Diamond) | 6.5 - 7.5 |
| Mixed reception (Alien: Covenant, X-Men: Apocalypse) | 6.0 - 6.5 |
| Poor reception (Assassin's Creed, Jonah Hex) | 5.0 - 5.5 |
| Unreleased / no votes | 0.0 |

### `vote_count` (int)

Number of user votes on TMDb. This is the strongest stable signal for whether a
film is widely known.

| Category | Typical range |
|---|---|
| Major blockbusters (Inception, Django Unchained) | 15,000 - 40,000+ |
| Well-known films (The Revenant, Once Upon a Time in Hollywood) | 5,000 - 15,000 |
| Recognisable films (Blood Diamond, Gangs of New York) | 1,500 - 8,000 |
| Niche but known (Eden Lake, Jane Eyre) | 500 - 2,000 |
| Obscure (The 11th Hour, Evel Knievel on Tour) | 0 - 100 |

### `original_language` (str)

ISO 639-1 language code for the film's original language (e.g. `"en"`, `"ko"`,
`"fr"`). Most Hollywood films are `"en"`. International co-productions may have
a non-English original language even if widely known in English markets.

### `genre_ids` (list of int)

TMDb genre IDs. Available on credit responses without a detail fetch.

| ID | Genre |
|---|---|
| 28 | Action |
| 12 | Adventure |
| 16 | Animation |
| 35 | Comedy |
| 80 | Crime |
| 99 | Documentary |
| 18 | Drama |
| 10751 | Family |
| 14 | Fantasy |
| 36 | History |
| 27 | Horror |
| 10402 | Music |
| 9648 | Mystery |
| 10749 | Romance |
| 878 | Science Fiction |
| 10770 | TV Movie |
| 53 | Thriller |
| 10752 | War |
| 37 | Western |

## Fields requiring a detail fetch

These fields are available on the full `Movie` model (from `/movie/{id}`) but
are **not** present on `MovieCreditRole` responses from
`/person/{id}/movie_credits`.

- `production_countries` -- list of `{iso_3166_1, name}`
- `spoken_languages` -- list of `{english_name, iso_639_1, name}`
- `genres` -- list of `{id, name}` (full objects, not just IDs)
- `runtime`, `budget`, `revenue`
- `belongs_to_collection`

Fetching these requires one API call per movie, which is expensive during puzzle
generation. Prefer filtering on the fields above when possible.

## Server-side filtering

The TMDb API offers almost no server-side filtering on the endpoints used by
artist-graph:

| Endpoint | Parameters |
|---|---|
| `/person/{id}/movie_credits` | `language` (response locale only) |
| `/movie/{id}/credits` | `language` (response locale only) |
| `/person/popular` | `language`, `page` |

The `language` parameter controls response localisation (e.g. translated
titles), not which results are returned. All filtering must be done client-side
after fetching results. See `MovieFilter` in
`art_graph.cinema_data_providers.filters`.
