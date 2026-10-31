import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv


load_dotenv()

model = ChatGroq(model = os.getenv("GROQ_MODEL"))