from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(f"Sua chave lida foi: {api_key}")
