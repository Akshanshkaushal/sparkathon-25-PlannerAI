from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

def get_budget_agent_chain():
    llm = AzureChatOpenAI(
        azure_deployment=os.environ.get('AZURE_OPENAI_GPT_DEPLOYMENT_NAME'),
        api_version=os.environ.get('AZURE_OPENAI_GPT_DEPLOYMENT_VERSION')
    )

    prompt_template = """
    You are a financial assistant. Your task is to create a budget for a planned event based on a user's spending habits.

    **User's Spending Tier:** {spending_tier}

    **Event Plan:**
    {event_plan_json}

    **Your Task:**
    - For each category in the event plan (gifts, decorations, cake), assign a reasonable budget range (min and max).
    - The total budget should align with the user's spending tier.

    **Output Format:**
    Provide your response as a JSON object where each key is a category from the event plan, and the value is another JSON object with "min_budget" and "max_budget".
    """

    prompt = PromptTemplate(template=prompt_template, input_variables=["spending_tier", "event_plan_json"])
    return LLMChain(llm=llm, prompt=prompt)