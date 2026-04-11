"""Tests for the Recommender class."""

import os
import sys

# Add src directory to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.recommender import Recommender, load_songs
from src.scoring_algorithms import (
    EnergyFocusedScorer,
    SimpleGenreScorer,
    WeightedScorer,
)
from src.song import Song
from src.user_preferences import UserProfile


def create_test_songs() -> list[Song]:
    """Create a small set of test songs."""
    return [
        Song(
            id=1,
            title="Happy Pop Song",
            artist="Pop Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Beat",
            artist="Lofi Producer",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
        Song(
            id=3,
            title="Intense Rock",
            artist="Rock Band",
            genre="rock",
            mood="intense",
            energy=0.9,
            tempo_bpm=150,
            valence=0.4,
            danceability=0.6,
            acousticness=0.1,
        ),
        Song(
            id=4,
            title="Jazz Relaxation",
            artist="Jazz Quartet",
            genre="jazz",
            mood="relaxed",
            energy=0.35,
            tempo_bpm=90,
            valence=0.7,
            danceability=0.4,
            acousticness=0.85,
        ),
    ]


def create_test_user(
    genre: str = "pop",
    mood: str = "happy",
    energy: float = 0.8,
    likes_acoustic: bool = False,
) -> UserProfile:
    """Create a test user profile."""
    return UserProfile(
        id=1,
        name="Test User",
        favorite_genre=genre,
        favorite_mood=mood,
        target_energy=energy,
        likes_acoustic=likes_acoustic,
    )


def test_recommender_initialization():
    """Test that Recommender initializes correctly."""
    songs = create_test_songs()
    recommender = Recommender(songs)

    assert len(recommender.songs) == 4
    assert isinstance(recommender.algorithm, WeightedScorer)


def test_recommender_initialization_with_custom_algorithm():
    """Test Recommender initialization with custom algorithm."""
    songs = create_test_songs()
    algorithm = SimpleGenreScorer()
    recommender = Recommender(songs, algorithm)

    assert recommender.algorithm == algorithm


def test_recommend_returns_correct_type():
    """Test that recommend returns list of tuples."""
    songs = create_test_songs()
    recommender = Recommender(songs)
    user = create_test_user(genre="pop", mood="happy")

    results = recommender.recommend(user, k=2)

    assert isinstance(results, list)
    assert len(results) == 2
    assert all(isinstance(r, tuple) and len(r) == 3 for r in results)


def test_recommend_returns_song_objects():
    """Test that recommendations return Song objects."""
    songs = create_test_songs()
    recommender = Recommender(songs)
    user = create_test_user()

    results = recommender.recommend(user, k=2)

    for song, score, explanation in results:
        assert isinstance(song, Song)
        assert isinstance(score, float)
        assert isinstance(explanation, str)


def test_recommend_returns_scores_in_descending_order():
    """Test that recommendations are sorted by score descending."""
    songs = create_test_songs()
    recommender = Recommender(songs)
    user = create_test_user(genre="pop", mood="happy", energy=0.8)

    results = recommender.recommend(user, k=4)

    scores = [score for _, score, _ in results]
    assert scores == sorted(scores, reverse=True)


def test_recommend_respects_k_parameter():
    """Test that k parameter limits results correctly."""
    songs = create_test_songs()
    recommender = Recommender(songs)
    user = create_test_user()

    for k in [1, 2, 3, 4]:
        results = recommender.recommend(user, k=k)
        assert len(results) == k


def test_recommend_k_greater_than_songs():
    """Test that k larger than available songs returns all songs."""
    songs = create_test_songs()
    recommender = Recommender(songs)
    user = create_test_user()

    results = recommender.recommend(user, k=10)

    assert len(results) == 4


def test_set_algorithm():
    """Test switching algorithm at runtime."""
    songs = create_test_songs()
    recommender = Recommender(songs, WeightedScorer())

    assert isinstance(recommender.algorithm, WeightedScorer)

    recommender.set_algorithm(SimpleGenreScorer())
    assert isinstance(recommender.algorithm, SimpleGenreScorer)

    recommender.set_algorithm(EnergyFocusedScorer())
    assert isinstance(recommender.algorithm, EnergyFocusedScorer)


def test_different_algorithms_produce_different_rankings():
    """Test that different algorithms rank songs differently."""
    songs = create_test_songs()
    user = create_test_user(genre="pop", mood="happy", energy=0.8)

    recommender_weighted = Recommender(songs, WeightedScorer())
    recommender_simple = Recommender(songs, SimpleGenreScorer())

    results_weighted = recommender_weighted.recommend(user, k=4)
    results_simple = recommender_simple.recommend(user, k=4)

    weighted_order = [song.id for song, _, _ in results_weighted]
    simple_order = [song.id for song, _, _ in results_simple]

    # Orders might be completely different
    assert weighted_order != simple_order


def test_pop_fan_recommendations():
    """Test recommendations for a pop music lover."""
    songs = create_test_songs()
    recommender = Recommender(songs, WeightedScorer())
    user = create_test_user(genre="pop", mood="happy", energy=0.8)

    results = recommender.recommend(user, k=1)

    # Should recommend the happy pop song first
    song, _, _ = results[0]
    assert song.genre == "pop"
    assert song.mood == "happy"


def test_lofi_chill_fan_recommendations():
    """Test recommendations for a lofi chill listener."""
    songs = create_test_songs()
    recommender = Recommender(songs, WeightedScorer())
    user = create_test_user(genre="lofi", mood="chill", energy=0.4)

    results = recommender.recommend(user, k=1)

    # Should recommend the chill lofi beat first
    song, _, _ = results[0]
    assert song.genre == "lofi" or song.energy <= 0.5


def test_rock_fan_recommendations():
    """Test recommendations for a rock lover."""
    songs = create_test_songs()
    recommender = Recommender(songs, WeightedScorer())
    user = create_test_user(genre="rock", mood="intense", energy=0.9)

    results = recommender.recommend(user, k=1)

    song, _, _ = results[0]
    # Should prefer the rock song
    assert song.genre == "rock" or song.energy >= 0.8


def test_jazz_fan_recommendations():
    """Test recommendations for a jazz lover."""
    songs = create_test_songs()
    recommender = Recommender(songs, WeightedScorer())
    user = create_test_user(
        genre="jazz", mood="relaxed", energy=0.3, likes_acoustic=True
    )

    results = recommender.recommend(user, k=1)

    song, _, _ = results[0]
    # Jazz or low-energy songs should rank high
    assert song.genre == "jazz" or song.energy <= 0.5


def test_acoustic_preference_affects_recommendations():
    """Test that acoustic preference affects recommendations."""
    songs = create_test_songs()
    recommender = Recommender(songs, WeightedScorer())

    user_likes_acoustic = create_test_user(genre="lofi", likes_acoustic=True)
    user_dislikes_acoustic = create_test_user(genre="lofi", likes_acoustic=False)

    results_acoustic = recommender.recommend(user_likes_acoustic, k=4)
    results_electric = recommender.recommend(user_dislikes_acoustic, k=4)

    # Different preferences should lead to different rankings
    acoustic_order = [score for _, score, _ in results_acoustic]
    electric_order = [score for _, score, _ in results_electric]

    assert acoustic_order != electric_order


def test_explanations_are_non_empty():
    """Test that score explanations are provided."""
    songs = create_test_songs()
    recommender = Recommender(songs)
    user = create_test_user()

    results = recommender.recommend(user, k=2)

    for _, _, explanation in results:
        assert explanation.strip() != ""
        assert len(explanation) > 0


def test_explanations_contain_reasons():
    """Test that explanations contain multiple reasons."""
    songs = create_test_songs()
    recommender = Recommender(songs)
    user = create_test_user()

    results = recommender.recommend(user, k=1)

    _, _, explanation = results[0]
    # Explanation should contain multiple reasons separated by |
    reasons = explanation.split("|")
    assert len(reasons) >= 2


def test_empty_k_returns_empty_list():
    """Test that k=0 returns empty list."""
    songs = create_test_songs()
    recommender = Recommender(songs)
    user = create_test_user()

    results = recommender.recommend(user, k=0)

    assert len(results) == 0


def test_all_scores_are_positive():
    """Test that all recommendation scores are positive."""
    songs = create_test_songs()
    recommender = Recommender(songs)
    user = create_test_user()

    results = recommender.recommend(user, k=4)

    for _, score, _ in results:
        assert score >= 0


def test_load_songs_from_csv():
    """Test loading songs from CSV file."""
    songs = load_songs("data/songs.csv")

    assert isinstance(songs, list)
    assert len(songs) > 0
    assert all(isinstance(s, Song) for s in songs)


def test_recommender_with_loaded_songs():
    """Test using Recommender with songs loaded from CSV."""
    songs = load_songs("data/songs.csv")

    recommender = Recommender(songs)
    user = create_test_user(genre="pop", mood="happy")

    results = recommender.recommend(user, k=5)

    assert len(results) == 5
    assert all(isinstance(s, Song) for s, _, _ in results)
