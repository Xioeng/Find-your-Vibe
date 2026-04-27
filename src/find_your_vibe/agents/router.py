"""Rule-based router for a lightweight agentic workflow."""

from .types import AgentAction, AgentDecision, AgentRequest


class SimpleAgentRouter:
    """Map user intent text to one of the supported actions."""

    def route(self, request: AgentRequest) -> AgentDecision:
        text = request.user_text.lower()

        if "spotify" in text or "track" in text or "artist" in text:
            return AgentDecision(
                action=AgentAction.FETCH_SPOTIFY,
                rationale="Detected Spotify or track-related intent.",
            )

        if "analy" in text or "trend" in text or "insight" in text:
            return AgentDecision(
                action=AgentAction.ANALYZE_TRACKS,
                rationale="Detected analysis intent.",
            )

        return AgentDecision(
            action=AgentAction.RECOMMEND,
            rationale="Defaulting to recommendation workflow.",
        )
