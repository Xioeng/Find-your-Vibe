"""Application settings helpers.

Supports local development and Streamlit Community Cloud secrets.
"""

import os
from dataclasses import dataclass


@dataclass
class AppSettings:
    """Typed container for external API credentials."""

    spotify_client_id: str | None
    spotify_client_secret: str | None
    google_api_key: str | None


def _read_streamlit_secret(key: str) -> str | None:
    """Read a key from Streamlit secrets when streamlit is available."""
    try:
        import streamlit as st
    except ImportError:
        return None

    value = st.secrets.get(key)
    return str(value) if value is not None else None


def _read_value(key: str) -> str | None:
    """Read from environment first, then Streamlit secrets."""
    return os.getenv(key) or _read_streamlit_secret(key)


def load_settings() -> AppSettings:
    """Build app settings from known configuration sources."""
    return AppSettings(
        spotify_client_id=_read_value("SPOTIFY_CLIENT_ID"),
        spotify_client_secret=_read_value("SPOTIFY_CLIENT_SECRET"),
        google_api_key=_read_value("GOOGLE_API_KEY"),
    )
