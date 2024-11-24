# Import dependencies
import feedparser
from pyfacebook import GraphAPI

from dotenv import load_dotenv
import os

version = 0.1

# Configuration
debug = True
agent = 'paperboy 0.1' # User agent for HTTP requests
url = 'https://www.chronicle-tribune.com/search/?k=%23free&f=atom&altf=mrss&ips=1080&l=100'

# Parse RSS feed
d = feedparser.parse(url, request_headers = {'User-agent':agent})

for entry in d.entries:
    title = entry.title
    link = entry.link
    
# Import environment variables
load_dotenv()
APP_ID = os.getenv("APP_ID")  # Your App ID
APP_SECRET = os.getenv("APP_SECRET")  # Your App secret
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")  # Your Access Token with the target page

# GraphAPI configuration
api = GraphAPI(
    app_id = APP_ID,
    app_secret = APP_SECRET,
    access_token = ACCESS_TOKEN
)