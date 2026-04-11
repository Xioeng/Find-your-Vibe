from dataclasses import dataclass


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """

    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

    @classmethod
    def from_dict(cls, data: dict) -> "Song":
        """Create a Song from a dictionary."""
        return cls(**data)

    def __str__(self):
        return f"{self.title} by {self.artist} [{self.genre}, {self.mood}]"
