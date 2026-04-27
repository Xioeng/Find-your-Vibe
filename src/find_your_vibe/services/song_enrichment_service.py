"""Song enrichment: MusicBrainz discovery + Gemini feature inference."""

from typing import Optional

from src.find_your_vibe.domain.song import Song
from src.find_your_vibe.services.llm_analyzer import GeminiAnalyzer
from src.find_your_vibe.services.spotify_client import MusicBrainzClient


class SongEnrichmentService:
    """
    Orchestrates song discovery and feature enrichment.

    Workflow:
    1. Search for songs using MusicBrainz (reliable, no auth required)
    2. Use Gemini to infer missing audio features (energy, mood, acousticness, etc.)
    3. Return complete Song objects with all required metadata
    """

    def __init__(self, gemini_api_key: Optional[str] = None) -> None:
        """
        Initialize the enrichment service.

        Args:
            gemini_api_key: Google Generative AI API key for feature inference
        """
        self.mb_client = MusicBrainzClient()
        self.analyzer = GeminiAnalyzer(api_key=gemini_api_key)

    def search_and_enrich(
        self, query: str, limit: int = 10, offset: int = 0
    ) -> list[Song]:
        """
        Search for songs and enrich them with audio features.

        Args:
            query: Search query (e.g., "pop happy", "jazz piano")
            limit: Maximum number of results to return
            offset: Pagination offset

        Returns:
            List of Song objects with complete metadata
        """
        # Step 1: Search for songs using MusicBrainz
        mb_songs = self.mb_client.request_songs(query=query, limit=limit, offset=offset)

        if not mb_songs:
            return []

        # Step 2: Enrich each song with Gemini features
        enriched_songs = []
        for mb_song in mb_songs:
            enriched = self._enrich_song(mb_song, query)
            if enriched:
                enriched_songs.append(enriched)

        return enriched_songs

    def _enrich_song(self, mb_song, query: str) -> Optional[Song]:
        """
        Enrich a MusicBrainz song with Gemini-inferred audio features.

        Args:
            mb_song: MusicBrainzSong object from search
            query: Original search query (used as fallback mood)

        Returns:
            Complete Song object with audio features, or None if enrichment fails
        """
        try:
            # Get Gemini's inferred audio features
            features = self.analyzer.infer_audio_features(mb_song.name, mb_song.artist)

            if not features:
                return None

            # Create Song object with all required fields
            song = Song(
                id=hash(f"{mb_song.id}_{mb_song.name}") % (10**9),  # Create numeric ID
                title=mb_song.name,
                artist=mb_song.artist,
                genre=self._infer_genre(query),  # Extract genre from query if possible
                mood=features.mood,
                energy=features.energy,
                tempo_bpm=features.tempo_bpm,
                valence=features.valence,
                danceability=features.danceability,
                acousticness=features.acousticness,
            )

            return song
        except Exception as e:
            print(f"Failed to enrich song '{mb_song.name}' by {mb_song.artist}: {e}")
            return None

    def _infer_genre(self, query: str) -> str:
        """
        Extract genre from search query if possible.

        Args:
            query: Search query (e.g., "pop happy", "jazz piano")

        Returns:
            Inferred genre or "unknown"
        """
        common_genres = [
            "pop",
            "rock",
            "jazz",
            "classical",
            "hip-hop",
            "electronic",
            "r&b",
            "folk",
            "metal",
            "indie",
            "country",
            "soul",
        ]

        query_lower = query.lower()
        for genre in common_genres:
            if genre in query_lower:
                return genre

        return "unknown"
