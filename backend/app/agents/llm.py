import os
from functools import lru_cache

from langchain_openai import AzureChatOpenAI


def is_llm_configured() -> bool:
    return bool(
        os.environ.get("AZURE_OPENAI_GPT_DEPLOYMENT_NAME")
        and os.environ.get("AZURE_OPENAI_GPT_DEPLOYMENT_VERSION")
        and os.environ.get("AZURE_OPENAI_API_KEY")
        and os.environ.get("AZURE_OPENAI_ENDPOINT")
    )


@lru_cache(maxsize=1)
def get_chat_model(temperature: float = 0.2) -> AzureChatOpenAI:
    """Central Azure OpenAI configuration for every agent."""
    deployment = os.environ.get("AZURE_OPENAI_GPT_DEPLOYMENT_NAME")
    api_version = os.environ.get("AZURE_OPENAI_GPT_DEPLOYMENT_VERSION")

    if not deployment:
        raise RuntimeError("AZURE_OPENAI_GPT_DEPLOYMENT_NAME is not configured.")
    if not api_version:
        raise RuntimeError("AZURE_OPENAI_GPT_DEPLOYMENT_VERSION is not configured.")

    return AzureChatOpenAI(
        azure_deployment=deployment,
        api_version=api_version,
        temperature=temperature,
        max_retries=2,
        timeout=45,
    )
