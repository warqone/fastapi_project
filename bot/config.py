import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_ID = os.getenv('ADMIN_ID', '0')
BOT_TOKEN = os.getenv('BOT_TOKEN')
API_URL = os.getenv('API_URL')
