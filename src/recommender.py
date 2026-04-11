"""
Music Recommender System with pluggable scoring algorithms.
"""

import pandas as pd

from .scoring_algorithms import ScoringAlgorithm, WeightedScorer
from .song import Song
from .user_preferences import UserProfile


def load_songs(csv_path: str) -> list[Song]:
    """
    Loads songs from a CSV file.

    Args:
        csv_path: Path to the CSV file containing songs.

    Returns:
        List of song dictionaries.
    """
    print(f"Loading songs from {csv_path}...")
    df = pd.read_csv(csv_path)
    songs = [Song.from_dict(s) for s in df.to_dict("records")]
    print(f"Loaded {len(songs)} songs.")
    return songs


class Recommender:
    """
    Recommender that uses pluggable scoring algorithms.

    This class orchestrates song recommendations using different scoring
    strategies that can be swapped at initialization or runtime.
    """

    def __init__(
        self, songs: list[Song], algorithm: ScoringAlgorithm | None = None
    ) -> None:
        """
        Initialize the recommender.

        Args:
            songs: List of Song objects.
            algorithm: Scoring algorithm to use. Defaults to WeightedScorer.
        """
        self.songs: list[Song] = songs
        self.algorithm: ScoringAlgorithm = algorithm or WeightedScorer()

    def set_algorithm(self, algorithm: ScoringAlgorithm) -> None:
        """
        Change the scoring algorithm at runtime.

        Args:
            algorithm: The new scoring algorithm to use.
        """
        self.algorithm = algorithm

    def recommend(
        self, user_prefs: UserProfile, k: int = 5
    ) -> list[tuple[Song, float, str]]:
        """
        Get top K recommendations using current algorithm.

        Args:
            user_prefs: UserProfile object with user preferences.
            k: Number of recommendations to return.

        Returns:
            List of (Song, score, explanation) tuples.
        """
        scored_songs: list[tuple[Song, float, str]] = []

        for song in self.songs:
            result = self.algorithm.score(user_prefs, song)
            explanation = " | ".join(result.reasons)
            scored_songs.append((song, result.score, explanation))

        # Sort by score descending
        scored_songs.sort(key=lambda x: x[1], reverse=True)

        return scored_songs[:k]
