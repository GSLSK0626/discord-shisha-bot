from dotenv import load_dotenv
import os

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DB_NAME = os.getenv('DB_NAME', 'shisha.db')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')