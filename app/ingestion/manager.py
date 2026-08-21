from google import generativeai as genai
from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer

from loaders.pdf_loader  import load_pdf
import os

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

llm = genai.GenerativeModel("gemini-2.5-flash")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

files = ["data/raw/untitled.pdf", "data/raw/sample2.pdf"]
