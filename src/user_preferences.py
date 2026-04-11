from dataclasses import dataclass


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """

    id: int
    name: str
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

    @classmethod
    def from_dict(cls, data: dict) -> "UserProfile":
        """Create a UserProfile from a dictionary."""
        return cls(**data)

    def __str__(self) -> str:
        """String representation of user profile."""
        acoustic_pref = (
            "likes acoustic" if self.likes_acoustic else ("dislikes acoustic")
        )
        return (
            f"User {self.name} (ID: {self.id}): Genre: {self.favorite_genre}, "
            f"Mood: {self.favorite_mood}, Energy: {self.target_energy}, "
            f"{acoustic_pref}"
        )
