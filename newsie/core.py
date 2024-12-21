# Import helper functions
import logging
from helpers import *

def main():

    # RSS Source Configuration
    source = FeedScraper(
        agent = 'newsie', # User agent for HTTP requests
        url = 'https://www.chronicle-tribune.com/search/?k=%23free&s=&f=atom&altf=mrss&ips=1080&l=100'
    )
    
    # Queue Configuration
    queue = QueueManager(
        posts_per_day = 6, # Number of posts per day (int)
        day_start = 7, # First post time (int)
        day_end = 18 # Last post time (int)
        )
    
    # Facebook Configuration (see .env for more)
    fb = FacebookPoster(
        page_id = "",
        )
    
    currency_limit = 2 # Max number of days after publish (int) 
    
    tracker = PostTracker()
    
    unposted_items = []
    unposted_ids = []
    
    entries = source.read_rss()

    for entry in entries:
        # If entry.id is not in posted_ids.json 
        if tracker.get_unposted_ids([entry.id]):
            # Add item dict and id to respective list
            unposted_items.append(entry)
            unposted_ids.append(entry.id)

    
    # Process unposted items
    if unposted_items:
        slots = queue.construct_queue()
        
        print(f"Found {len(unposted_items)} unposted items")
        
        fb.create_posts(unposted_items, slots)
        # fb.add_to_queue(unposted_items)
                    
        # After successful posting, mark as posted
        # tracker.mark_as_posted(unposted_ids) 

if __name__ == '__main__':
    main()