from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

def get_goal_agent_chain():
    llm = AzureChatOpenAI(
        azure_deployment=os.environ.get('AZURE_OPENAI_GPT_DEPLOYMENT_NAME'),
        api_version="2023-05-15" # Check your Azure OpenAI Studio for the correct version
    )

    prompt_template = """
    You are a creative event planner. Your task is to generate a comprehensive plan for an upcoming event.

    **Event Details:**
    - **Event Type:** {event_type}
    - **Honoree:** {person_name}
    - **User Preferences for {person_name}:** {user_preferences}

    **Your Plan Should Include:**
    1.  **Gift Suggestions:**
        -   Three specific gift ideas directly related to the user's stated preferences.
        -   Two "inspired-by" gift ideas that are related to but not explicitly listed in the preferences. For each, provide a brief reason why the honoree might like it.
    2.  **Decoration Theme:**
        -   Suggest a creative decoration theme.
        -   List five essential decoration items for this theme.
    3.  **Cake Suggestion:**
        -   Recommend a type of cake and a suitable size for a party of approximately 10-15 people.

    **Output Format:**
    Provide your response as a JSON object with the following keys: "gift_suggestions", "decoration_theme", "decoration_items", "cake_suggestion".
    """

    prompt = PromptTemplate(template=prompt_template, input_variables=["event_type", "person_name", "user_preferences"])
    return LLMChain(llm=llm, prompt=prompt)