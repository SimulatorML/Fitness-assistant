from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY") #Добавили

if google_api_key:
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key, temperature=0, convert_system_message_to_human=True)
elif openai_api_key: #Добавили
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL_NAME", "gpt-4"), openai_api_key=openai_api_key, temperature=0
    )
else:
    raise ValueError("Neither GOOGLE_API_KEY nor OPENAI_API_KEY are set")