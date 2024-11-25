# Import dependencies
import feedparser
from pyfacebook import GraphAPI

from dotenv import load_dotenv
import os

from helpers import PostTracker

def main():

    version = 0.1

    # Configuration
    debug = True
    agent = 'paperboy 0.1' # User agent for HTTP requests
    url = 'https://www.chronicle-tribune.com/search/?k=%23free&s=&f=atom&altf=mrss&ips=1080&l=100'

    # Parse RSS feed
    d = feedparser.parse(url, request_headers = {'User-agent':agent})

    # Initialize post tracker
    tracker = PostTracker()
    
    unposted_items = []
    unposted_ids = []

    for entry in d.entries:
        if tracker.get_unposted_ids([entry.id]):
            unposted_items.append(entry)
            unposted_ids.append(entry.id)

    # Process unposted items
    if unposted_items:
        print(f"Found {len(unposted_items)} unposted items")
        
        for item in unposted_items:
            """
            additional logic here
            """
            
        # After successful posting, mark as posted
        # tracker.mark_as_posted(unposted_ids) 
        
    # Import environment variables
    load_dotenv()
    APP_ID = os.getenv("APP_ID")  # Your App ID
    APP_SECRET = os.getenv("APP_SECRET")  # Your App secret
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")  # Your Access Token with the target page

    # GraphAPI configuration
    fb = GraphAPI(
        app_id = APP_ID,
        app_secret = APP_SECRET,
        access_token = ACCESS_TOKEN
    )

if __name__ == '__main__':
    main()