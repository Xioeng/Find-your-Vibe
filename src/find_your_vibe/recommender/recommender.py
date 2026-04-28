"""
Music Recommender System with pluggable scoring algorithms.
"""

from ..domain import Song, UserProfile
from .scoring_algorithms import ScoringAlgorithm, WeightedScorer


class Recommender:
    """
    Recommender that uses pluggable scoring algorithms.

    This class orchestrates song recommendations using different scoring
    strategies that can be swapped at initialization or runtime.
    """

    def __init__(
        self, songs: list[Song], algorithm: ScoringAlgorithm = WeightedScorer()
    ) -> None:
        """
        Initialize the recommender.

        Args:
            songs: List of Song objects.
            algorithm: Scoring algorithm to use. Defaults to WeightedScorer.
        """
        self.songs: list[Song] = songs
        self.algorithm: ScoringAlgorithm = algorithm

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
