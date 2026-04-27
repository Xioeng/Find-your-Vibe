"""Tests for the Song class."""

from src.find_your_vibe.domain import Song


def test_song_creation():
    """Test creating a Song object."""
    song = Song(
        id=1,
        title="Test Song",
        artist="Test Artist",
        genre="pop",
        mood="happy",
        energy=0.8,
        tempo_bpm=120,
        valence=0.9,
        danceability=0.8,
        acousticness=0.2,
    )

    assert song.id == 1
    assert song.title == "Test Song"
    assert song.artist == "Test Artist"
    assert song.genre == "pop"
    assert song.mood == "happy"
    assert song.energy == 0.8
    assert song.tempo_bpm == 120
    assert song.valence == 0.9
    assert song.danceability == 0.8
    assert song.acousticness == 0.2


def test_song_from_dict():
    """Test creating a Song from a dictionary."""
    song_data = {
        "id": 1,
        "title": "Test Song",
        "artist": "Test Artist",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "tempo_bpm": 120,
        "valence": 0.9,
        "danceability": 0.8,
        "acousticness": 0.2,
    }

    song = Song.from_dict(song_data)

    assert song.id == 1
    assert song.title == "Test Song"
    assert song.genre == "pop"


def test_song_str_representation():
    """Test the string representation of a Song."""
    song = Song(
        id=1,
        title="Test Song",
        artist="Test Artist",
        genre="pop",
        mood="happy",
        energy=0.8,
        tempo_bpm=120,
        valence=0.9,
        danceability=0.8,
        acousticness=0.2,
    )

    assert "Test Song" in str(song)
    assert "Test Artist" in str(song)
    assert "pop" in str(song)
    assert "happy" in str(song)


def test_song_with_different_genres():
    """Test creating songs with different genres."""
    genres = ["pop", "rock", "jazz", "lofi", "ambient", "electronic"]

    for genre in genres:
        song = Song(
            id=1,
            title="Test",
            artist="Test",
            genre=genre,
            mood="happy",
            energy=0.5,
            tempo_bpm=100,
            valence=0.7,
            danceability=0.6,
            acousticness=0.3,
        )
        assert song.genre == genre


def test_song_with_different_moods():
    """Test creating songs with different moods."""
    moods = ["happy", "chill", "intense", "relaxed", "peaceful", "energetic"]

    for mood in moods:
        song = Song(
            id=1,
            title="Test",
            artist="Test",
            genre="pop",
            mood=mood,
            energy=0.5,
            tempo_bpm=100,
            valence=0.7,
            danceability=0.6,
            acousticness=0.3,
        )
        assert song.mood == mood


def test_song_energy_range():
    """Test songs with various energy levels."""
    energies = [0.0, 0.25, 0.5, 0.75, 1.0]

    for energy in energies:
        song = Song(
            id=1,
            title="Test",
            artist="Test",
            genre="pop",
            mood="happy",
            energy=energy,
            tempo_bpm=100,
            valence=0.7,
            danceability=0.6,
            acousticness=0.3,
        )
        assert song.energy == energy


def test_song_numeric_attributes():
    """Test that numeric attributes are stored correctly."""
    song = Song(
        id=42,
        title="Test",
        artist="Test",
        genre="pop",
        mood="happy",
        energy=0.85,
        tempo_bpm=135,
        valence=0.92,
        danceability=0.88,
        acousticness=0.15,
    )

    assert song.id == 42
    assert song.energy == 0.85
    assert song.tempo_bpm == 135
    assert song.valence == 0.92
    assert song.danceability == 0.88
    assert song.acousticness == 0.15
