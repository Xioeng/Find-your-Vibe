"""Pytest configuration and shared fixtures."""

import pytest

from src.find_your_vibe.domain import Song, UserProfile


@pytest.fixture
def sample_songs() -> list[Song]:
    """Fixture providing a standard set of test songs."""
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


@pytest.fixture
def pop_user() -> UserProfile:
    """Fixture providing a pop music lover."""
    return UserProfile(
        id=1,
        name="Pop Fan",
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )


@pytest.fixture
def jazz_user() -> UserProfile:
    """Fixture providing a jazz music lover."""
    return UserProfile(
        id=2,
        name="Jazz Lover",
        favorite_genre="jazz",
        favorite_mood="relaxed",
        target_energy=0.35,
        likes_acoustic=True,
    )


@pytest.fixture
def rock_user() -> UserProfile:
    """Fixture providing a rock music lover."""
    return UserProfile(
        id=3,
        name="Rock Fan",
        favorite_genre="rock",
        favorite_mood="intense",
        target_energy=0.9,
        likes_acoustic=False,
    )


@pytest.fixture
def lofi_user() -> UserProfile:
    """Fixture providing a lofi music lover."""
    return UserProfile(
        id=4,
        name="Lofi Chiller",
        favorite_genre="lofi",
        favorite_mood="chill",
        target_energy=0.4,
        likes_acoustic=True,
    )
