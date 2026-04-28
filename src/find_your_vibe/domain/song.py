from dataclasses import dataclass


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """

    id: int = 0
    title: str = "Unknown Title"
    artist: str = "Unknown Artist"
    energy: float = 0.5  # 0.0-1.0
    mood: str = "neutral"  # "happy", "sad", "energetic", "calm", etc.
    valence: float = 0.5  # 0.0-1.0 (musical positiveness)
    danceability: float = 0.5  # 0.0-1.0
    acousticness: float = 0.5  # 0.0-1.0
    tempo_bpm: int = 120  # beats per minute (estimate)
    genre: str = "unknown"  # Inferred genre or style (e.g., "rock", "pop", "jazz", "hip-hop", etc.)

    @classmethod
    def from_dict(cls, data: dict) -> "Song":
        """Create a Song from a dictionary."""
        return cls(**data)

    def __str__(self):
        return f"{self.title} by {self.artist} [{self.genre}, {self.mood}]"
