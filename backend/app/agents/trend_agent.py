import os
import json
import logging
import re
from langchain_openai import AzureChatOpenAI

logger = logging.getLogger(__name__)


def extract_json_from_markdown(text):
    """
    Extract JSON from text that might be wrapped in markdown code blocks.
    """
    # Check for code blocks with ```json ... ``` format
    code_block_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
    if code_block_match:
        return code_block_match.group(1).strip()
    return text.strip()


def run_trend_ai(product_list: list, budget: dict, category: str) -> dict:
    """
    Uses OpenAI to suggest the best product from a given list within budget.
    Returns a structured JSON recommendation.
    """
    llm = AzureChatOpenAI(
        temperature=0,
        azure_deployment=os.environ.get('AZURE_OPENAI_GPT_DEPLOYMENT_NAME'),
        api_version=os.environ.get('AZURE_OPENAI_GPT_DEPLOYMENT_VERSION')
    )

    # Build direct prompt
    user_prompt = f"""
You are a shopping expert.

Category: {category}
Budget: {budget}

Here is a list of product options already gathered:

{json.dumps(product_list, indent=2)}

Your task:
- Pick the best product under the budget.
- If none are under budget, suggest a realistic product with an estimated price.

Return STRICTLY JSON ONLY in this format with no markdown formatting, no code blocks, just the raw JSON:
{{
  "source": "Existing Products" or "Created Suggestion",
  "title": "Product Title",
  "price": {{
    "currentPrice": "100.00",
    "currency": "$"
  }},
  "link": "https://product-link.com",
  "reviewsCount": "200" or "N/A",
  "isBestSeller": true or false
}}
"""

    logger.info(f"📤 Sending trend AI prompt for category '{category}' with budget {budget}...")

    # Run the LLM
    response = llm.invoke(user_prompt)
    
    # Access content correctly from AIMessage
    response_text = response.content
    
    logger.debug(f"Raw response from trend AI: {response_text}")
    
    # Extract JSON from possible markdown formatting
    extracted_json = extract_json_from_markdown(response_text)
    logger.debug(f"Extracted JSON: {extracted_json}")

    # Parse
    try:
        return json.loads(extracted_json)
    except json.JSONDecodeError as e:
        logger.error(f"❌ Could not parse JSON from trend AI. Error: {str(e)}. Raw:\n{response_text}")
        return {
            "source": "Error",
            "title": f"No valid recommendation for {category}",
            "price": {
                "currentPrice": "0.00",
                "currency": "$"
            },
            "link": "",
            "reviewsCount": "N/A",
            "isBestSeller": False
        }


# Add backward compatibility function if needed
def create_trend_agent_executor():
    """
    For backward compatibility with existing imports.
    Returns a callable that wraps run_trend_ai.
    """
    return lambda product_list, budget, category: run_trend_ai(product_list, budget, category)
