from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# for now we use only OpenAI
llm = ChatOpenAI(
    model="gpt-4",
    openai_api_key = os.getenv("OPENAI_API_KEY"),
    temperature=0
)
