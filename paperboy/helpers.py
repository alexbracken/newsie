import json
import os
from typing import List, Set
from dotenv import load_dotenv
from pyfacebook import GraphAPI
import feedparser
from datetime import datetime, timedelta

class PostTracker:
    def __init__(self, tracking_file: str = 'posted.json'):
        """
        Initialize a tracker to prevent duplicate posts.
        
        :param tracking_file: Path to file storing posted IDs
        """
        self.tracking_file = tracking_file
        self.posted_ids = self._load_posted_ids()
    
    def _load_posted_ids(self) -> Set[str]:
        """
        Load previously posted IDs from file.
        
        :return: Set of posted IDs
        """
        try:
            # Create tracking file if it doesn't exist
            if not os.path.exists(self.tracking_file):
                with open(self.tracking_file, 'w') as f:
                    json.dump([], f)
            
            # Read existing posted IDs
            with open(self.tracking_file, 'r') as f:
                return set(json.load(f))
        
        except (json.JSONDecodeError, IOError) as e:
            # Log error or print if debug mode is on
            print(f"Error loading posted IDs: {e}")
            return set()
    
    def _save_posted_ids(self):
        """
        Save posted IDs to file.
        """
        try:
            with open(self.tracking_file, 'w') as f:
                json.dump(list(self.posted_ids), f)
        except IOError as e:
            print(f"Error saving posted IDs: {e}")
    
    def get_unposted_ids(self, new_ids: List[str]) -> List[str]:
        """
        Filter out IDs that have already been posted.
        
        :param new_ids: List of new item IDs to check
        :return: List of IDs that have not been posted before
        """
        return [
            item_id for item_id in new_ids 
            if item_id not in self.posted_ids
        ]
    
    def mark_as_posted(self, ids: List[str], max_tracked_ids: int = 1000):
        """
        Mark the given IDs as posted.
        
        :param ids: List of IDs to mark as posted
        :param max_tracked_ids: Maximum number of IDs to keep track of
        """
        # Add new IDs to the set
        self.posted_ids.update(ids)
        
        # Limit the number of tracked IDs
        if len(self.posted_ids) > max_tracked_ids:
            self.posted_ids = set(list(self.posted_ids)[-max_tracked_ids:])
        
        # Save to file
        self._save_posted_ids()

class FacebookPoster:

    def _create_queue(self, posts_per_day: int, day_start: int, day_end: int) -> List:
        """
        Create queue for Facebook posting
        
        :param posts_per_day: Number of posts/day
        :param day_start: First post time in 24H format
        :param day_end: Last post time in 24H format
        
        :return: List of slots for posts
        """
        #  
        if posts_per_day == 1:
            return [day_start]
        
        # Calculate interval between slots
        n = (day_end - day_start) / (posts_per_day - 1)
        
        slots = [day_start + i * n for i in range(posts_per_day)]
    
        # Ensure last slot is exactly day_end
        slots[-1] = day_end
        
        return slots
    
    def create_posts(self, unposted_items: List[dict], page_id: str):
        
        # Import environment variables
        load_dotenv()
        
        # GraphAPI configuration
        fb = GraphAPI(
            app_id = os.getenv("APP_ID"),
            app_secret = os.getenv("APP_SECRET"),
            access_token=os.getenv("ACCESS_TOKEN")
        )
        # TODO Create posting logic
        for item in unposted_items:
            
            params= {"fields": "id,message,created_time,from"},
            
            # Test for existence of items
            if 'title' in item:
                title = item.title
            link = item.link
            summary = item.summary
            
            post: dict = {
                'body': summary,
            }
            
            """
            fb.post_object(
                page_id,
                connection="feed",
                data={
                    "message": "This is a tests message by api"
                    },
            )
            """
            

class FeedScraper:
    def read_rss(self, url: str, agent: str) -> List[dict]:
        """
        Scrape RSS feeds
        
        :param ids: List of IDs to mark as posted
        :param max_tracked_ids: Maximum number of IDs to keep track of
        """
        
        url = url
        agent = agent
        d = feedparser.parse(
            url,
            request_headers = {'User-agent':agent}
        )
        
        return d.entries