import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')

CHANNEL_ID = os.getenv('CHANNEL_ID')
OPENAI_API_KEY = os.getenv('openai.api_key')
CHANNEL_ID_MAIN = os.getenv('CHANNEL_ID_MAIN')