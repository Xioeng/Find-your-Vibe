"""MusicBrainz integration helpers.

This module provides a minimal client for searching songs (recordings).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import musicbrainzngs


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

    def discover_artist_singles(self, artist_name: str, limit: int = 10) -> list[dict]:
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
