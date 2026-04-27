"""
Scoring algorithms for the Music Recommender System.

This module contains different strategies for scoring songs based on user preferences.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..domain import Song, UserProfile


@dataclass
class ScoringResult:
    """Result of scoring a song."""

    score: float
    reasons: list[str]


class ScoringAlgorithm(ABC):
    """Abstract base class for scoring algorithms."""

    @abstractmethod
    def score(self, user_prefs: UserProfile, song: Song) -> ScoringResult:
        """Score a song against user preferences."""
        pass


class WeightedScorer(ScoringAlgorithm):
    """Original weighted scoring from README."""

    def score(self, user_prefs: UserProfile, song: Song) -> ScoringResult:
        """Score using weighted combination of features."""
        reasons: list[str] = []

        # Genre match
        genre_match = (
            1.0 if song.genre.lower() == user_prefs.favorite_genre.lower() else 0.5
        )
        if genre_match == 1.0:
            reasons.append(f"Genre '{song.genre}' matches")
        else:
            reasons.append(f"Genre '{song.genre}' partial match")

        # Mood match
        mood_match = (
            1.0 if song.mood.lower() == user_prefs.favorite_mood.lower() else 0.5
        )
        if mood_match == 1.0:
            reasons.append(f"Mood '{song.mood}' matches")
        else:
            reasons.append(f"Mood '{song.mood}' partial match")

        # Energy match
        energy_diff = abs(song.energy - user_prefs.target_energy)
        energy_match = 1.0 - min(energy_diff, 0.5)
        reasons.append(f"Energy close to target (diff: {energy_diff:.2f})")

        # Acousticness preference
        acousticness = song.acousticness
        acoustic_score = (
            acousticness if user_prefs.likes_acoustic else (1.0 - acousticness)
        )

        # Danceability
        danceability = song.danceability

        # Calculate final score
        score = 100 * (
            0.35 * genre_match
            + 0.30 * mood_match
            + 0.20 * energy_match
            + 0.10 * acoustic_score
            + 0.05 * danceability
        )

        return ScoringResult(score=score, reasons=reasons)


class SimpleGenreScorer(ScoringAlgorithm):
    """Simple algorithm: just match genre and mood."""

    def score(self, user_prefs: UserProfile, song: Song) -> ScoringResult:
        """Score using only genre and mood matching."""
        reasons: list[str] = []

        genre_match = (
            1.0 if song.genre.lower() == user_prefs.favorite_genre.lower() else 0.0
        )
        mood_match = (
            1.0 if song.mood.lower() == user_prefs.favorite_mood.lower() else 0.0
        )

        score = 100 * (0.6 * genre_match + 0.4 * mood_match)

        if genre_match == 1.0:
            reasons.append("Genre matches perfectly")
        else:
            reasons.append(f"Genre '{song.genre}' doesn't match")

        if mood_match == 1.0:
            reasons.append("Mood matches perfectly")
        else:
            reasons.append(f"Mood '{song.mood}' doesn't match")

        return ScoringResult(score=score, reasons=reasons)


class EnergyFocusedScorer(ScoringAlgorithm):
    """Prioritizes energy level matching."""

    def score(self, user_prefs: UserProfile, song: Song) -> ScoringResult:
        """Score prioritizing energy matching."""
        reasons: list[str] = []

        energy_diff = abs(song.energy - user_prefs.target_energy)
        energy_match = 1.0 - min(energy_diff, 0.5)

        genre_match = (
            1.0 if song.genre.lower() == user_prefs.favorite_genre.lower() else 0.5
        )
        danceability = song.danceability

        score = 100 * (0.50 * energy_match + 0.30 * genre_match + 0.20 * danceability)

        reasons.append(f"Energy match: {energy_match:.2f} (diff: {energy_diff:.2f})")
        reasons.append(f"Genre: {song.genre}")
        reasons.append(f"Danceability: {danceability:.2f}")

        return ScoringResult(score=score, reasons=reasons)
