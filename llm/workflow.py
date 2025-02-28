from langchain.prompts import PromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from langchain.chains import LLMChain
from llm.models import llm  

SYSTEM_PROMPT = """
You are an AI fitness assistant. Your job is to provide users with expert-level fitness, nutrition, and workout recommendations.
You should personalize responses based on the user's fitness level, goals, and other relevant details.
Be precise, encouraging, and professional. Keep answers concise but informative.
"""

prompt_template = PromptTemplate(
    input_variables=["user_info", "query"],
    template="User Info: {user_info}\nUser Question: {query}"
)

def process_fitness_query(user_query: str, user_info: dict) -> str:
    """
    Processes a user query with user info and returns an AI-generated response.

    Args:
        user_query (str): The fitness-related question asked by the user.
        user_info (dict): Additional details about the user (e.g., age, fitness level, goals).

    Returns:
        str: The AI-generated response.
    """
    # Combine system instructions with user input
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=prompt_template.format(user_info=user_info, query=user_query))
    ]
    
    chain = LLMChain(llm=llm, prompt=prompt_template)

    response = chain.run({"user_info": user_info, "query": user_query})

    return response
