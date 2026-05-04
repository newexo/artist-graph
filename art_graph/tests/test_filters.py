from datetime import date

from art_graph.cinema_data_providers.filters import MovieFilter
from art_graph.cinema_data_providers.tmdb_models import MovieCreditRole


def make_movie(**overrides) -> MovieCreditRole:
    """Create a MovieCreditRole with sensible defaults for testing."""
    defaults = dict(
        id=100,
        title="Test Movie",
        original_language="en",
        popularity=20.0,
        vote_average=7.0,
        vote_count=500,
        genre_ids=[28, 12],  # Action, Adventure
        release_date=date(2020, 6, 15),
    )
    defaults.update(overrides)
    return MovieCreditRole(**defaults)


class TestMovieFilterDefaults:
    def test_accepts_typical_english_movie(self):
        f = MovieFilter()
        assert f.accepts(make_movie()) is True

    def test_rejects_non_english_by_default(self):
        f = MovieFilter()
        assert f.accepts(make_movie(original_language="ko")) is False

    def test_rejects_documentary_by_default(self):
        f = MovieFilter()
        assert f.accepts(make_movie(genre_ids=[99])) is False

    def test_rejects_tv_movie_by_default(self):
        f = MovieFilter()
        assert f.accepts(make_movie(genre_ids=[10770])) is False


class TestLanguageFilter:
    def test_empty_set_accepts_all_languages(self):
        f = MovieFilter(allowed_languages=set())
        assert f.accepts(make_movie(original_language="ko")) is True
        assert f.accepts(make_movie(original_language="fr")) is True
        assert f.accepts(make_movie(original_language="en")) is True

    def test_multiple_allowed_languages(self):
        f = MovieFilter(allowed_languages={"en", "fr"})
        assert f.accepts(make_movie(original_language="en")) is True
        assert f.accepts(make_movie(original_language="fr")) is True
        assert f.accepts(make_movie(original_language="de")) is False


class TestVoteFilter:
    def test_min_vote_average(self):
        f = MovieFilter(min_vote_average=5.0)
        assert f.accepts(make_movie(vote_average=7.0)) is True
        assert f.accepts(make_movie(vote_average=5.0)) is True
        assert f.accepts(make_movie(vote_average=4.9)) is False

    def test_min_vote_count(self):
        f = MovieFilter(min_vote_count=100)
        assert f.accepts(make_movie(vote_count=500)) is True
        assert f.accepts(make_movie(vote_count=100)) is True
        assert f.accepts(make_movie(vote_count=99)) is False

    def test_zero_vote_count_accepted_by_default(self):
        f = MovieFilter()
        assert f.accepts(make_movie(vote_count=0)) is True


class TestPopularityFilter:
    def test_min_popularity(self):
        f = MovieFilter(min_popularity=10.0)
        assert f.accepts(make_movie(popularity=20.0)) is True
        assert f.accepts(make_movie(popularity=10.0)) is True
        assert f.accepts(make_movie(popularity=9.9)) is False


class TestGenreFilter:
    def test_excluded_genre_rejects(self):
        f = MovieFilter(excluded_genre_ids={99})
        assert f.accepts(make_movie(genre_ids=[99])) is False

    def test_mixed_genres_one_excluded(self):
        f = MovieFilter(excluded_genre_ids={99})
        assert f.accepts(make_movie(genre_ids=[28, 99])) is False

    def test_no_excluded_genres_accepts_all(self):
        f = MovieFilter(excluded_genre_ids=set())
        assert f.accepts(make_movie(genre_ids=[99, 10770])) is True

    def test_empty_genre_ids_accepted(self):
        f = MovieFilter(excluded_genre_ids={99})
        assert f.accepts(make_movie(genre_ids=[])) is True

    def test_none_genre_ids_accepted(self):
        f = MovieFilter(excluded_genre_ids={99})
        assert f.accepts(make_movie(genre_ids=None)) is True


class TestCombinedFilters:
    def test_all_criteria_must_pass(self):
        f = MovieFilter(
            allowed_languages={"en"},
            min_vote_average=5.0,
            min_vote_count=50,
            min_popularity=10.0,
            excluded_genre_ids={99},
        )
        # Passes everything
        assert f.accepts(make_movie()) is True

    def test_fails_on_language_despite_other_criteria(self):
        f = MovieFilter(
            allowed_languages={"en"},
            min_vote_average=5.0,
        )
        assert f.accepts(make_movie(original_language="ja", vote_average=9.0)) is False

    def test_fails_on_vote_despite_other_criteria(self):
        f = MovieFilter(min_vote_average=6.0)
        assert f.accepts(make_movie(vote_average=3.0, original_language="en")) is False

    def test_permissive_filter_accepts_everything(self):
        f = MovieFilter(
            allowed_languages=set(),
            min_vote_average=0.0,
            min_vote_count=0,
            min_popularity=0.0,
            excluded_genre_ids=set(),
        )
        assert (
            f.accepts(
                make_movie(original_language="zh", vote_average=1.0, genre_ids=[99])
            )
            is True
        )
