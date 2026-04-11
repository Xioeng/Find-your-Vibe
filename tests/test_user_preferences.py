"""Tests for the UserProfile class."""

from src.user_preferences import UserProfile


def test_user_profile_creation():
    """Test creating a UserProfile object."""
    user = UserProfile(
        id=1,
        name="Pop Fan",
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )

    assert user.id == 1
    assert user.name == "Pop Fan"
    assert user.favorite_genre == "pop"
    assert user.favorite_mood == "happy"
    assert user.target_energy == 0.8
    assert user.likes_acoustic is False


def test_user_profile_from_dict():
    """Test creating a UserProfile from a dictionary."""
    user_data = {
        "id": 1,
        "name": "Jazz Lover",
        "favorite_genre": "jazz",
        "favorite_mood": "relaxed",
        "target_energy": 0.4,
        "likes_acoustic": True,
    }

    user = UserProfile.from_dict(user_data)

    assert user.id == 1
    assert user.name == "Jazz Lover"
    assert user.favorite_genre == "jazz"
    assert user.favorite_mood == "relaxed"
    assert user.target_energy == 0.4
    assert user.likes_acoustic is True


def test_user_profile_str_representation_likes_acoustic():
    """Test string representation for user who likes acoustic."""
    user = UserProfile(
        id=1,
        name="Acoustic Lover",
        favorite_genre="folk",
        favorite_mood="peaceful",
        target_energy=0.3,
        likes_acoustic=True,
    )

    user_str = str(user)
    assert "Acoustic Lover" in user_str
    assert "folk" in user_str
    assert "peaceful" in user_str
    assert "likes acoustic" in user_str


def test_user_profile_str_representation_dislikes_acoustic():
    """Test string representation for user who dislikes acoustic."""
    user = UserProfile(
        id=2,
        name="Electronic Fan",
        favorite_genre="electronic",
        favorite_mood="energetic",
        target_energy=0.9,
        likes_acoustic=False,
    )

    user_str = str(user)
    assert "Electronic Fan" in user_str
    assert "electronic" in user_str
    assert "energetic" in user_str
    assert "dislikes acoustic" in user_str


def test_user_profile_different_genres():
    """Test creating users with different favorite genres."""
    genres = ["pop", "rock", "jazz", "lofi", "folk", "electronic"]

    for i, genre in enumerate(genres):
        user = UserProfile(
            id=i,
            name=f"User {i}",
            favorite_genre=genre,
            favorite_mood="happy",
            target_energy=0.5,
            likes_acoustic=False,
        )
        assert user.favorite_genre == genre


def test_user_profile_different_moods():
    """Test creating users with different favorite moods."""
    moods = ["happy", "chill", "intense", "relaxed", "peaceful"]

    for i, mood in enumerate(moods):
        user = UserProfile(
            id=i,
            name=f"User {i}",
            favorite_genre="pop",
            favorite_mood=mood,
            target_energy=0.5,
            likes_acoustic=False,
        )
        assert user.favorite_mood == mood


def test_user_profile_energy_levels():
    """Test users with different target energy levels."""
    energies = [0.2, 0.4, 0.6, 0.8, 1.0]

    for i, energy in enumerate(energies):
        user = UserProfile(
            id=i,
            name=f"User {i}",
            favorite_genre="pop",
            favorite_mood="happy",
            target_energy=energy,
            likes_acoustic=False,
        )
        assert user.target_energy == energy


def test_user_profile_acoustic_preference():
    """Test users with different acoustic preferences."""
    user_likes_acoustic = UserProfile(
        id=1,
        name="Acoustic Lover",
        favorite_genre="folk",
        favorite_mood="peaceful",
        target_energy=0.3,
        likes_acoustic=True,
    )

    user_dislikes_acoustic = UserProfile(
        id=2,
        name="Electric Lover",
        favorite_genre="electronic",
        favorite_mood="energetic",
        target_energy=0.8,
        likes_acoustic=False,
    )

    assert user_likes_acoustic.likes_acoustic is True
    assert user_dislikes_acoustic.likes_acoustic is False


def test_user_profile_id_and_name():
    """Test that user ID and name are set correctly."""
    user = UserProfile(
        id=42,
        name="Test User",
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.5,
        likes_acoustic=False,
    )

    assert user.id == 42
    assert user.name == "Test User"
