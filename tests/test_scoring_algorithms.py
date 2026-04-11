"""Tests for the scoring algorithms."""

from src.scoring_algorithms import (
    EnergyFocusedScorer,
    ScoringResult,
    SimpleGenreScorer,
    WeightedScorer,
)
from src.song import Song
from src.user_preferences import UserProfile


def create_test_song(
    genre: str = "pop",
    mood: str = "happy",
    energy: float = 0.8,
    acousticness: float = 0.2,
    danceability: float = 0.8,
) -> Song:
    """Helper function to create a test song."""
    return Song(
        id=1,
        title="Test Song",
        artist="Test Artist",
        genre=genre,
        mood=mood,
        energy=energy,
        tempo_bpm=120,
        valence=0.9,
        danceability=danceability,
        acousticness=acousticness,
    )


def create_test_user(
    genre: str = "pop",
    mood: str = "happy",
    energy: float = 0.8,
    likes_acoustic: bool = False,
) -> UserProfile:
    """Helper function to create a test user."""
    return UserProfile(
        id=1,
        name="Test User",
        favorite_genre=genre,
        favorite_mood=mood,
        target_energy=energy,
        likes_acoustic=likes_acoustic,
    )


class TestWeightedScorer:
    """Tests for WeightedScorer algorithm."""

    def test_scoring_result_structure(self):
        """Test that scoring returns proper ScoringResult."""
        scorer = WeightedScorer()
        song = create_test_song()
        user = create_test_user()

        result = scorer.score(user, song)

        assert isinstance(result, ScoringResult)
        assert isinstance(result.score, float)
        assert isinstance(result.reasons, list)
        assert len(result.reasons) > 0

    def test_perfect_match_scores_high(self):
        """Test that perfect match scores high."""
        scorer = WeightedScorer()
        song = create_test_song(genre="pop", mood="happy", energy=0.8)
        user = create_test_user(genre="pop", mood="happy", energy=0.8)

        result = scorer.score(user, song)

        assert result.score > 80

    def test_no_match_scores_lower(self):
        """Test that mismatched preferences score lower."""
        scorer = WeightedScorer()
        song = create_test_song(genre="rock", mood="intense")
        user = create_test_user(genre="pop", mood="happy")

        result = scorer.score(user, song)

        assert result.score < 80

    def test_genre_match_affects_score(self):
        """Test that matching genre increases score."""
        scorer = WeightedScorer()
        song_match = create_test_song(genre="pop")
        song_no_match = create_test_song(genre="rock")
        user = create_test_user(genre="pop")

        result_match = scorer.score(user, song_match)
        result_no_match = scorer.score(user, song_no_match)

        assert result_match.score > result_no_match.score

    def test_mood_match_affects_score(self):
        """Test that matching mood increases score."""
        scorer = WeightedScorer()
        song_match = create_test_song(mood="happy")
        song_no_match = create_test_song(mood="chill")
        user = create_test_user(mood="happy")

        result_match = scorer.score(user, song_match)
        result_no_match = scorer.score(user, song_no_match)

        assert result_match.score > result_no_match.score

    def test_energy_similarity_affects_score(self):
        """Test that similar energy levels score higher."""
        scorer = WeightedScorer()
        song_match = create_test_song(energy=0.8)
        song_no_match = create_test_song(energy=0.2)
        user = create_test_user(energy=0.8)

        result_match = scorer.score(user, song_match)
        result_no_match = scorer.score(user, song_no_match)

        assert result_match.score > result_no_match.score

    def test_acoustic_preference_with_likes_acoustic(self):
        """Test that acoustic lovers prefer acoustic songs."""
        scorer = WeightedScorer()
        song_acoustic = create_test_song(acousticness=0.9)
        song_electric = create_test_song(acousticness=0.1)
        user = create_test_user(likes_acoustic=True)

        result_acoustic = scorer.score(user, song_acoustic)
        result_electric = scorer.score(user, song_electric)

        assert result_acoustic.score > result_electric.score

    def test_acoustic_preference_with_dislikes_acoustic(self):
        """Test that electric music lovers prefer electric songs."""
        scorer = WeightedScorer()
        song_acoustic = create_test_song(acousticness=0.9)
        song_electric = create_test_song(acousticness=0.1)
        user = create_test_user(likes_acoustic=False)

        result_acoustic = scorer.score(user, song_acoustic)
        result_electric = scorer.score(user, song_electric)

        assert result_electric.score > result_acoustic.score

    def test_score_range(self):
        """Test that scores are in reasonable range (0-100)."""
        scorer = WeightedScorer()
        song = create_test_song()
        user = create_test_user()

        result = scorer.score(user, song)

        assert 0 <= result.score <= 100

    def test_reasons_non_empty(self):
        """Test that reasons list contains explanations."""
        scorer = WeightedScorer()
        song = create_test_song()
        user = create_test_user()

        result = scorer.score(user, song)

        assert len(result.reasons) >= 3  # At least genre, mood, energy


class TestSimpleGenreScorer:
    """Tests for SimpleGenreScorer algorithm."""

    def test_simple_scorer_perfect_match(self):
        """Test simple scorer with perfect genre and mood match."""
        scorer = SimpleGenreScorer()
        song = create_test_song(genre="pop", mood="happy")
        user = create_test_user(genre="pop", mood="happy")

        result = scorer.score(user, song)

        assert result.score == 100

    def test_simple_scorer_no_match(self):
        """Test simple scorer with no matches."""
        scorer = SimpleGenreScorer()
        song = create_test_song(genre="rock", mood="intense")
        user = create_test_user(genre="pop", mood="happy")

        result = scorer.score(user, song)

        assert result.score == 0

    def test_simple_scorer_genre_only_match(self):
        """Test simple scorer with only genre match."""
        scorer = SimpleGenreScorer()
        song = create_test_song(genre="pop", mood="intense")
        user = create_test_user(genre="pop", mood="happy")

        result = scorer.score(user, song)

        assert result.score == 60  # 0.6 * 100

    def test_simple_scorer_mood_only_match(self):
        """Test simple scorer with only mood match."""
        scorer = SimpleGenreScorer()
        song = create_test_song(genre="rock", mood="happy")
        user = create_test_user(genre="pop", mood="happy")

        result = scorer.score(user, song)

        assert result.score == 40  # 0.4 * 100


class TestEnergyFocusedScorer:
    """Tests for EnergyFocusedScorer algorithm."""

    def test_energy_focused_prioritizes_energy(self):
        """Test that energy-focused scorer prioritizes energy match."""
        scorer = EnergyFocusedScorer()
        user = create_test_user(genre="rock", energy=0.8)

        # Song with matching energy but different genre
        song_energy_match = create_test_song(genre="pop", energy=0.8)
        # Song with matching genre but different energy
        song_genre_match = create_test_song(genre="rock", energy=0.2)

        result_energy = scorer.score(user, song_energy_match)
        result_genre = scorer.score(user, song_genre_match)

        # Energy match should score higher
        assert result_energy.score > result_genre.score

    def test_energy_focused_low_energy_user(self):
        """Test energy-focused scorer with low energy preference."""
        scorer = EnergyFocusedScorer()
        user = create_test_user(energy=0.2)
        song_low = create_test_song(energy=0.2)
        song_high = create_test_song(energy=0.8)

        result_low = scorer.score(user, song_low)
        result_high = scorer.score(user, song_high)

        assert result_low.score > result_high.score

    def test_energy_focused_high_energy_user(self):
        """Test energy-focused scorer with high energy preference."""
        scorer = EnergyFocusedScorer()
        user = create_test_user(energy=0.9)
        song_high = create_test_song(energy=0.9)
        song_low = create_test_song(energy=0.1)

        result_high = scorer.score(user, song_high)
        result_low = scorer.score(user, song_low)

        assert result_high.score > result_low.score


def test_different_scorers_produce_different_results():
    """Test that different algorithms produce different scores."""
    song = create_test_song(genre="pop", mood="happy", energy=0.8)
    user = create_test_user(genre="rock", mood="intense", energy=0.2)

    weighted = WeightedScorer().score(user, song)
    simple = SimpleGenreScorer().score(user, song)
    energy = EnergyFocusedScorer().score(user, song)

    # All scores should be different
    scores = [weighted.score, simple.score, energy.score]
    assert len(set(scores)) == 3  # All unique
