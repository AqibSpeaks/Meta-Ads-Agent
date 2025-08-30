import os
from dotenv import load_dotenv

load_dotenv()

# Meta API Configuration (You'll need to get these from Meta Developer Portal)
META_APP_ID = os.getenv('META_APP_ID')
META_APP_SECRET = os.getenv('META_APP_SECRET')
META_ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')

# OpenAI Configuration (for AI insights)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Default settings
DEFAULT_COUNTRIES = ['US', 'GB', 'CA', 'AU', 'DE', 'FR']
DEFAULT_CATEGORIES = ['POLITICS', 'ECOMMERCE', 'HEALTH', 'TECH', 'EDUCATION']

# API Endpoints
META_API_BASE = "https://graph.facebook.com/v18.0"
ADS_ENDPOINT = f"{META_API_BASE}/ads_archive"
