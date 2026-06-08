from __future__ import annotations

from datetime import datetime
from typing import Any

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, messages_from_dict, messages_to_dict


class MongoRecipientMemory(BaseChatMessageHistory):
    """LangChain chat history backed by the recipient document in MongoDB."""

    def __init__(self, db_service: Any, summary: str):
        self.db_service = db_service
        self.summary = summary

    @property
    def messages(self) -> list[BaseMessage]:
        user_doc = self.db_service.get_user_by_summary(self.summary) or {}
        raw_messages = user_doc.get("conversation_memory", [])
        if not raw_messages:
            return []
        return messages_from_dict(raw_messages)

    def add_message(self, message: BaseMessage) -> None:
        current_messages = self.messages
        current_messages.append(message)
        self.db_service.create_or_update_event_user(
            self.summary,
            {
                "conversation_memory": messages_to_dict(current_messages[-16:]),
                "memory_updated_at": datetime.utcnow().isoformat(),
            },
        )

    def clear(self) -> None:
        self.db_service.create_or_update_event_user(
            self.summary,
            {
                "conversation_memory": [],
                "memory_updated_at": datetime.utcnow().isoformat(),
            },
        )

    def remember_turn(self, user_text: str, agent_text: str) -> None:
        self.add_message(HumanMessage(content=user_text))
        self.add_message(AIMessage(content=agent_text))


def summarize_memory(messages: list[BaseMessage], max_items: int = 8) -> str:
    recent = messages[-max_items:]
    if not recent:
        return "No prior conversation memory."

    lines = []
    for message in recent:
        role = "User" if isinstance(message, HumanMessage) else "Assistant"
        lines.append(f"{role}: {message.content}")
    return "\n".join(lines)
