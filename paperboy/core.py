# Import helper functions
from helpers import *
from datetime import time

def main():

    version = 0.1

    # General Configuration
    agent = 'paperboy 0.1' # User agent for HTTP requests
    url = 'https://www.chronicle-tribune.com/search/?k=%23free&s=&f=atom&altf=mrss&ips=1080&l=100'
    page_id = "263380803530734" # ID of target page
    
    # Queue Configuration
    posts_per_day = 6 # Number of posts per day (int)
    day_start = 7 # First post time
    day_end = 18 # Last post time 
    
    # Initialize feed scraper function
    d = feedparser.parse(url, request_headers = {'User-agent':agent})
    
    tracker = PostTracker()
    
    unposted_items = []
    unposted_ids = []
    
    # Iterate through entries
    for entry in d.entries:
        # If entry.id is not in posted_ids.json 
        if tracker.get_unposted_ids([entry.id]):
            # Add item dict and id to respective list
            unposted_items.append(entry)
            unposted_ids.append(entry.id)

    
    # Process unposted items
    if unposted_items:
        fb = FacebookPoster()
        slots = fb._create_queue(posts_per_day, day_start, day_end)
        
        print(f"Found {len(unposted_items)} unposted items")
        
        fb.create_posts(unposted_items, page_id)
        # fb.add_to_queue(unposted_items)
                    
        # After successful posting, mark as posted
        # tracker.mark_as_posted(unposted_ids) 

if __name__ == '__main__':
    main()