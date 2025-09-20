


import getpass
import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyCNlGZtW2sSLwB69KBoXK8gyhIEJRZQ6jc"

from langchain.chat_models import init_chat_model

model = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

response = model.invoke("Whats the current version of LangChain?")
print(response)