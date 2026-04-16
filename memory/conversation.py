import uuid
import logging
from collections import defaultdict
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Message:
    role: str  # "user" or "assistant"
    content: str


class ConversationStore:
    """In-memory conversation storage, keyed by session_id."""

    def __init__(self, max_history: int = 10):
        self._sessions: dict[str, list[Message]] = defaultdict(list)
        self.max_history = max_history

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = []
        logger.info(f"Created session: {session_id}")
        return session_id

    def add_message(self, session_id: str, role: str, content: str):
        self._sessions[session_id].append(Message(role=role, content=content))
        # Keep only recent history to manage memory
        max_messages = self.max_history * 2  # user + assistant pairs
        if len(self._sessions[session_id]) > max_messages:
            self._sessions[session_id] = self._sessions[session_id][-max_messages:]

    def get_history(self, session_id: str) -> list[Message]:
        return self._sessions.get(session_id, [])

    def format_history_for_prompt(self, session_id: str) -> str:
        """Format recent conversation history as a string for the LLM prompt."""
        messages = self.get_history(session_id)
        if not messages:
            return ""
        lines = []
        for msg in messages[-self.max_history * 2 :]:
            prefix = "User" if msg.role == "user" else "Assistant"
            lines.append(f"{prefix}: {msg.content}")
        return "\n".join(lines)

    def session_exists(self, session_id: str) -> bool:
        return session_id in self._sessions


# Module-level singleton
conversation_store = ConversationStore()
