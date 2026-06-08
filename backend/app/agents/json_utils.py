import json
import logging
import re
from typing import Any

logger = logging.getLogger(__name__)


def extract_json(text: str) -> str:
    """Return JSON text from a raw LLM response that may include markdown fences."""
    if not text:
        return "{}"

    code_block_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if code_block_match:
        return code_block_match.group(1).strip()

    start = min(
        [pos for pos in [text.find("{"), text.find("[")] if pos >= 0],
        default=0,
    )
    end = max(text.rfind("}"), text.rfind("]"))
    if end >= start:
        return text[start : end + 1].strip()
    return text.strip()


def parse_json(text: str, fallback: Any, context: str = "LLM response") -> Any:
    try:
        return json.loads(extract_json(text))
    except json.JSONDecodeError:
        logger.exception("Could not parse JSON from %s. Raw response: %s", context, text)
        return fallback
