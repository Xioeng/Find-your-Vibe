"""LLM-based analysis utilities for music data."""

import json
from dataclasses import dataclass
from typing import Optional

import google.genai as genai


@dataclass
class AudioFeatures:
    """Container for inferred audio features from Gemini."""

    energy: float  # 0.0-1.0
    mood: str  # "happy", "sad", "energetic", "calm", etc.
    valence: float  # 0.0-1.0 (musical positiveness)
    danceability: float  # 0.0-1.0
    acousticness: float  # 0.0-1.0
    tempo_bpm: int  # beats per minute (estimate)


class GeminiAnalyzer:
    """Wrapper around Gemini API for music feature inference.

    Uses LLM to intelligently infer audio features like energy, mood,
    danceability, acousticness from song title and artist name.
    """

    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model
        self.client = None
        if api_key:
            self.client = genai.Client(api_key=api_key)

    def is_configured(self) -> bool:
        """Return whether an API key is available."""
        return bool(self.api_key and self.client)

    def infer_audio_features_batch(self, songs: list[dict]) -> list[AudioFeatures]:
        """Infer audio features for multiple songs in a single prompt.

        Args:
            songs: List of dicts with 'title' and 'artist' keys

        Returns:
            List of AudioFeatures (one per song, in same order)
        """
        if not self.is_configured():
            raise ValueError("Gemini API not configured")

        if not songs:
            return []

        prompt = self._build_batch_feature_inference_prompt(songs)
        print(f"\n📝 Batch prompt ({len(songs)} songs):")
        print("=" * 60)
        print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
        print("=" * 60)

        response = self.client.models.generate_content(
            model=self.model, contents=prompt
        )

        print("\n📊 Gemini response:")
        print("=" * 60)
        response_text = response.text
        text_preview = (
            response_text[:500] + "..." if len(response_text) > 500 else response_text
        )
        print(text_preview)
        print("=" * 60)

        return self._parse_batch_features_from_response(response.text, len(songs))

    def _build_batch_feature_inference_prompt(self, songs: list[dict]) -> str:
        """Build prompt to infer features for multiple songs at once."""
        songs_text = "\n".join(
            f"{i + 1}. {song.get('title', 'Unknown')} by {song.get('artist', 'Unknown')}"
            for i, song in enumerate(songs)
        )

        return f"""Analyze these {len(songs)} songs and infer their audio features.
Return ONLY a valid JSON array with one object per song, in the same order as the list below.
No markdown, no explanation, just the JSON array.

Songs:
{songs_text}

Return JSON array (one object per song):
[
    {{
        "energy": <float 0-1>,
        "mood": "<string: happy, sad, energetic, calm, melancholic, uplifting, dark, neutral, etc>",
        "valence": <float 0-1>,
        "danceability": <float 0-1>,
        "acousticness": <float 0-1>,
        "tempo_bpm": <int 60-200>
    }},
    ... (one object for each song)
]

Guidelines:
- energy: How intense/powerful (0=quiet, 1=intense)
- mood: Dominant emotional tone
- valence: Musical positiveness (0=sad, 1=happy)
- danceability: How suitable for dancing (0=not danceable, 1=very danceable)
- acousticness: Acoustic vs electronic (0=electric, 1=acoustic)
- tempo_bpm: Estimated beats per minute

Example response for 2 songs:
[
    {{
        "energy": 0.8,
        "mood": "energetic",
        "valence": 0.9,
        "danceability": 0.95,
        "acousticness": 0.0,
        "tempo_bpm": 128
    }},
    {{
        "energy": 0.4,
        "mood": "calm",
        "valence": 0.7,
        "danceability": 0.2,
        "acousticness": 0.8,
        "tempo_bpm": 80
    }}
]
"""

    def _parse_batch_features_from_response(
        self, response_text: str, num_songs: int
    ) -> list[AudioFeatures]:
        """Parse AudioFeatures array from Gemini response."""
        try:
            # Clean up response
            json_str = response_text.strip()
            if "```" in json_str:
                json_str = json_str.split("```")[1]
                if json_str.startswith("json"):
                    json_str = json_str[4:]

            data_array = json.loads(json_str.strip())

            if not isinstance(data_array, list):
                raise ValueError("Response is not a JSON array")

            features_list = []
            for i, data in enumerate(data_array):
                if i >= num_songs:
                    break

                features = AudioFeatures(
                    energy=float(data.get("energy", 0.5)),
                    mood=str(data.get("mood", "neutral")),
                    valence=float(data.get("valence", 0.5)),
                    danceability=float(data.get("danceability", 0.5)),
                    acousticness=float(data.get("acousticness", 0.5)),
                    tempo_bpm=int(data.get("tempo_bpm", 120)),
                )
                features_list.append(features)

            return features_list
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            print(f"Failed to parse batch response: {e}")
            raise

    def summarize_tracks(self, track_names: list[str]) -> str:
        """Create a simple summary for a list of track names."""
        if not track_names:
            return "No tracks available to analyze."
        sample = ", ".join(track_names[:5])
        return f"Quick trend summary based on tracks: {sample}."
