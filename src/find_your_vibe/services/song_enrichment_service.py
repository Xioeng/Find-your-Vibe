"""Song enrichment: MusicBrainz discovery + Gemini feature inference.
TODO: Merge with ArtistDiscoveryService and refactor to avoid duplication with batch enrichment in llm_analyzer.py"""

from src.find_your_vibe.domain.song import Song
from src.find_your_vibe.services.llm_analyzer import GeminiAnalyzer
from src.find_your_vibe.services.music_client import MusicBrainzClient


class SongEnrichmentService:
    """
    Orchestrates song discovery and feature enrichment.

    Workflow:
    1. Search for songs using MusicBrainz (reliable, no auth required)
    2. Use Gemini to infer missing audio features (energy, mood, acousticness, etc.)
    3. Return complete Song objects with all required metadata
    """

    def __init__(self, gemini_api_key: str, model: str) -> None:
        """
        Initialize the enrichment service.

        Args:
            gemini_api_key: Google Generative AI API key for feature inference
            model: The Gemini model to use (e.g., "gemini-3.1-flash-lite-preview")
        """
        self.mb_client = MusicBrainzClient()
        self.analyzer = GeminiAnalyzer(api_key=gemini_api_key, model=model)
