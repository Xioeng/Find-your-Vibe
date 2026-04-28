"""Artist-based song discovery pipeline for music recommender system.

This service orchestrates the complete pipeline:
1. Gemini recommends artists based on user profile
2. MusicBrainz finds artist IDs and their single songs
3. Gemini enriches songs with audio features
4. Returns ~100-200 enriched songs for recommendation
"""

import json

import musicbrainzngs

from src.find_your_vibe.domain.song import Song
from src.find_your_vibe.domain.user_preferences import UserProfile
from src.find_your_vibe.services.llm_analyzer import GeminiAnalyzer
from src.find_your_vibe.services.music_client import MusicBrainzClient


class ArtistDiscoveryService:
    """Discovers and enriches songs through artist recommendations.

    Pipeline:
    1. Analyze user profile → recommend artists (via Gemini)
    2. Search artists in MusicBrainz → get artist IDs
    3. Browse singles per artist → collect ~100-200 songs
    4. Enrich with features → return complete Song objects
    """

    def __init__(self, gemini_api_key: str, model: str) -> None:
        """Initialize the discovery service.

        Args:
            gemini_api_key: Google Generative AI API key
            model: The Gemini model to use
        """
        self.api_key = gemini_api_key
        self.model = model
        self.analyzer = GeminiAnalyzer(api_key=gemini_api_key, model=model)
        self.mb_client = MusicBrainzClient()

    def discover_songs_for_user(
        self,
        user_profile: UserProfile,
        artists_per_query: int = 10,
        songs_per_artist: int = 10,
    ) -> list[Song]:
        """
        Discover songs tailored to user preferences.

        Args:
            user_profile: User's preferences and history
            artists_per_query: Number of artists to recommend (~10)
            songs_per_artist: Number of singles per artist (~10)

        Returns:
            List of 100-200 enriched Song objects with audio features
        """
        print(f"\n🎵 Discovering songs for {user_profile.name}...")

        # Step 1: Get artist recommendations from Gemini
        print("  1️⃣  Gemini recommending artists...")
        artists = self._recommend_artists(user_profile, artists_per_query)

        if not artists:
            print("  ❌ No artists recommended")
            return []

        print(f"  ✓ Recommended {len(artists)} artists: {', '.join(artists)}")

        # Step 2: Discover songs from each artist
        print("  2️⃣  Searching MusicBrainz for singles...")
        all_songs = []
        for artist_name in artists:
            songs = self.mb_client.discover_artist_singles(
                artist_name, limit=songs_per_artist
            )
            all_songs.extend(songs)
            print(f"     ✓ {artist_name}: {len(songs)} songs")

        print(f"  ✓ Found {len(all_songs)} total songs")

        # Step 3: Enrich ALL songs with audio features (BATCH)
        print(f"  3️⃣  Batch enriching {len(all_songs)} songs with Gemini...")
        enriched_songs = self._enrich_songs_batch(all_songs)

        print(f"  ✓ Enriched {len(enriched_songs)} songs")
        return enriched_songs

    def _recommend_artists(
        self, user_profile: UserProfile, num_artists: int = 10
    ) -> list[str]:
        """Use Gemini to recommend artists based on user profile."""
        prompt = self._build_artist_recommendation_prompt(user_profile, num_artists)

        response = self.analyzer.client.models.generate_content(
            model=self.model, contents=prompt
        )

        return self._parse_artist_recommendations(response.text)

    def _discover_artist_singles(self, artist_name: str, limit: int = 10) -> list[dict]:
        """
        Find single songs by a given artist using MusicBrainz.

        Args:
            artist_name: Name of the artist
            limit: Maximum songs to retrieve per artist

        Returns:
            List of song dictionaries with metadata
        """
        try:
            # Search for the artist to get their MusicBrainz ID
            artist_search = musicbrainzngs.search_artists(query=artist_name, limit=1)

            if not artist_search.get("artist-list"):
                return []

            artist_id = artist_search["artist-list"][0]["id"]

            # Browse all release-groups (singles) by this artist
            release_groups = musicbrainzngs.browse_release_groups(
                artist=artist_id, release_type=["single"], limit=limit
            )

            songs = []
            for release_group in release_groups.get("release-group-list", []):
                song = {
                    "id": release_group.get("id"),
                    "title": release_group.get("title", "Unknown"),
                    "artist": artist_name,
                    "artist_id": artist_id,
                    "type": release_group.get("type"),
                }
                songs.append(song)

            return songs

        except Exception as e:
            print(f"  ⚠️  MusicBrainz error for '{artist_name}': {e}")
            return []

    def _enrich_songs_batch(self, songs: list[dict]) -> list[Song]:
        """Enrich multiple songs with audio features in a single Gemini call.

        Args:
            songs: List of song dicts with title and artist

        Returns:
            List of complete Song objects
        """
        if not songs:
            return []

        try:
            # Get all features in one batch call
            features_list = self.analyzer.infer_audio_features_batch(songs)

            enriched_songs = []
            for song, features in zip(songs, features_list):
                if features:
                    enriched = Song(
                        id=hash(f"{song['id']}_{song['title']}") % (10**9),
                        title=song["title"],
                        artist=song["artist"],
                        genre=features.genre,
                        mood=features.mood,
                        energy=features.energy,
                        tempo_bpm=features.tempo_bpm,
                        valence=features.valence,
                        danceability=features.danceability,
                        acousticness=features.acousticness,
                    )
                    enriched_songs.append(enriched)

            return enriched_songs
        except Exception as e:
            print(f"Error enriching songs batch: {e}")
            raise

    def _build_artist_recommendation_prompt(
        self, user_profile: UserProfile, num_artists: int
    ) -> str:
        """Build prompt for Gemini to recommend artists.

        Args:
            user_profile: User's preferences
            num_artists: Target number of artists

        Returns:
            Prompt string for Gemini
        """
        song_history = ""
        if user_profile.song_list:
            song_history = ", ".join(
                [f"{song.title} by {song.artist}" for song in user_profile.song_list]
            )

        acoustic_text = (
            "Likes acoustic"
            if user_profile.likes_acoustic
            else "Prefers electric/produced"
        )

        return f"""You are a music expert. Recommend {num_artists} artists.
Based on the user profile, suggest well-known artists that match their
preferences and past likes. Include artists that the user likes already.

User: {user_profile.name}
- Favorite Genre: {user_profile.favorite_genre}
- Favorite Mood: {user_profile.favorite_mood}
- Target Energy: {user_profile.target_energy} (0-1)
- Acoustic: {acoustic_text}
- Liked Songs or Artists: {song_history}

Return ONLY JSON array with artist names. No markdown:
["Artist 1", "Artist 2", "Artist 3", ...]
"""

    def _parse_artist_recommendations(self, response_text: str) -> list[str]:
        """Parse artist names from Gemini response."""
        json_str = response_text.strip()
        if "```" in json_str:
            json_str = json_str.split("```")[1]
            if json_str.startswith("json"):
                json_str = json_str[4:]

        artists = json.loads(json_str.strip())
        if isinstance(artists, list):
            return [str(a).strip() for a in artists if a]
        return []
