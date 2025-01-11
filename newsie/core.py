# Import helper functions
import logging
from helpers import *

def main():

    # RSS Source Configuration
    source = FeedScraper(
        agent = 'newsie',
        url = 'https://www.heraldpalladium.com/search/',
        params = {
            'k': '#free',
            'q': 'news',
            't': 'article',
            'f': 'atom',
            'altf': 'mrss',
            'nsa': 'eedition',
        }
    )
    
    # Queue Configuration
    queue = QueueManager(
        posts_per_day = 6,
        day_start = 7,
        day_end = 18
        )
    
    # Facebook Configuration (see .env for more)
    fb = FacebookPoster(
        page_id = "568163179705403",
        post_type = "image",
        kicker = "Read more:",
        )
    # Max number of days after publish (int) 
    currency_limit = 2 
    
    tracker = PostTracker()
    
    unposted_items = []
    unposted_ids = []

    for entry in source.entries:
        # If entry.id is not in posted_ids.json 
        if tracker.get_unposted_ids([entry.id]):
            # Add item dict and id to respective list
            unposted_items.append(entry)
            unposted_ids.append(entry.id)

    
    # Process unposted items
    if unposted_items:
        slots = queue._construct_queue()

        fb.send_posts(slots, unposted_items)
        # After successful posting, mark as posted
        
        tracker.mark_as_posted(unposted_ids) 

if __name__ == '__main__':
    main()