"""MusicBrainz integration helpers.

This module provides a minimal client for searching songs (recordings).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import musicbrainzngs


@dataclass
class MusicBrainzSong:
    """Minimal song fields returned by MusicBrainz queries."""

    id: str
    name: str
    artist: str
    source_query: str | None = None


class MusicBrainzClient:
    """Minimal MusicBrainz client for requesting songs."""

    def __init__(
        self,
        app_name: str = "find-your-vibe",
        app_version: str = "0.1.0",
        contact: str = "student@example.com",
    ) -> None:
        self.app_name = app_name
        self.app_version = app_version
        self.contact = contact
        musicbrainzngs.set_useragent(
            self.app_name, self.app_version, contact=self.contact
        )

    def request_songs(
        self, query: str, limit: int = 10, offset: int = 0
    ) -> list[MusicBrainzSong]:
        """Request songs from MusicBrainz recording search."""
        if not query.strip() or limit <= 0:
            return []

        # try:
        result = musicbrainzngs.search_recordings(
            query=query, limit=min(limit, 100), offset=max(offset, 0)
        )
        # except Exception:
        #     return []

        items = result.get("recording-list", []) if result else []
        return [self._to_song(item, query) for item in items]

    def _to_song(self, item: dict[str, Any], query: str) -> MusicBrainzSong:
        """Convert MusicBrainz recording response to MusicBrainzSong."""
        artist_credit = item.get("artist-credit", [])
        artist_names = []
        for part in artist_credit:
            if isinstance(part, dict):
                artist_names.append(part.get("name", "Unknown"))
            elif isinstance(part, str):
                # Handle separator strings like " feat. "
                pass
        return MusicBrainzSong(
            id=item.get("id", ""),
            name=item.get("title", item.get("name", "Unknown Track")),
            artist=", ".join(artist_names) if artist_names else "Unknown Artist",
            source_query=query,
        )
