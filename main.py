"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender with different
scoring algorithms.
"""

from src.find_your_vibe.domain import Song, UserProfile
from src.find_your_vibe.recommender import (
    EnergyFocusedScorer,
    Recommender,
    SimpleGenreScorer,
    WeightedScorer,
    load_songs,
)


def main() -> None:
    # Load songs
    songs: list[Song] = load_songs("data/songs.csv")

    # Create recommender with default algorithm
    recommender: Recommender = Recommender(songs, WeightedScorer())

    # Define users
    users_data = [
        {
            "id": 1,
            "name": "Pop Enthusiast",
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.8,
            "likes_acoustic": False,
        },
        {
            "id": 2,
            "name": "Jazz Lover",
            "favorite_genre": "jazz",
            "favorite_mood": "relaxed",
            "target_energy": 0.4,
            "likes_acoustic": True,
        },
        {
            "id": 3,
            "name": "Rock Fan",
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.9,
            "likes_acoustic": False,
        },
    ]
    users: list[UserProfile] = [UserProfile.from_dict(u) for u in users_data]

    # Test different algorithms
    algorithms = [
        ("Weighted Genre Scorer", WeightedScorer()),
        ("Simple Genre Scorer", SimpleGenreScorer()),
        ("Energy Focused Scorer", EnergyFocusedScorer()),
    ]

    for user in users:
        print(f"\n{'=' * 60}")
        print(f"User: {user.name}")
        print(f"{'=' * 60}")

        for algo_name, algorithm in algorithms:
            recommender.set_algorithm(algorithm)

            print(f"\n--- Using {algo_name} ---")
            recommendations = recommender.recommend(user, k=5)

            for song, score, explanation in recommendations:
                print(song)
                print(f"  Score: {score:.2f}")
                print(f"  {explanation}\n")


if __name__ == "__main__":
    main()
