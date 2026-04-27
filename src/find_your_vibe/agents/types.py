"""Shared data types for the agent workflow."""

from dataclasses import dataclass
from enum import Enum


class AgentAction(str, Enum):
    """Supported high-level actions for the simple router."""

    FETCH_SPOTIFY = "fetch_spotify"
    ANALYZE_TRACKS = "analyze_tracks"
    RECOMMEND = "recommend"


@dataclass
class AgentRequest:
    """Input sent to the simple agent router."""

    user_text: str


@dataclass
class AgentDecision:
    """Router decision with optional rationale text."""

    action: AgentAction
    rationale: str
