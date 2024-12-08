import json
import os
from typing import List, Set
from dotenv import load_dotenv
from pyfacebook import GraphAPI
import feedparser
import logging

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
    
class QueueManager():
    def __init__(self, posts_per_day: int, day_start: int, day_end: int):
        """
        Initialize queue manager
        
        :param posts_per_day: Number of posts/day
        :param day_start: First post time in 24H format
        :param day_end: Last post time in 24H format
        """
        self.posts_per_day = posts_per_day
        self.day_start = day_start
        self.day_end = day_end
        
        self.construct_queue()
     
    def construct_queue(self) -> List[float]:
        """
        Create queue for Facebook posting
        
        :return: List of slots for posts
        """
        # Handle edge case for one post per day
        if self.posts_per_day == 1:
            return [self.day_start]
        
        n = (self.day_end - self.day_start) / (self.posts_per_day - 1)
        slots = [self.day_start + i * n for i in range(self.posts_per_day)]
        slots[-1] = self.day_end # Ensure last slot is exactly day_end

        return slots

class FacebookPoster():
    def __init__(self, page_id: str):
        """
        Initialize Facebook Poster
        
        :param page_id: Target Facebook page ID
        :param queue: Queue settings from create_queue method
        """
        self.page_id = page_id
        
    def _organize_posts(self):
        unposted_items = self.unposted_items
        
    def create_posts(self, unposted_items: List[dict], slots: List):
        for item in unposted_items:
            
            params= {"fields": "id,message,created_time,from"},
            
            # Test for existence of items
            if 'title' in item:
                title = item.title
            if 'link' in item:
                link = item.link
            if 'summary' in item:
                summary = item.summary
            
            data: dict = {
                'message': summary,
                'published': "false"
                
            }
        
    def send_posts(self):
        page_id = self.page_id
        
        # Import environment variables
        load_dotenv()
        
        # GraphAPI configuration
        fb = GraphAPI(
            app_id = os.getenv("APP_ID"),
            app_secret = os.getenv("APP_SECRET"),
            access_token=os.getenv("ACCESS_TOKEN")
        )
        """"
        fb.post_object(
            page_id,
            data,
            connection="feed",
        )
        """    

class FeedScraper:
    def __init__(self, url: str, agent: str):
        """
        Initialize FeedScraper instance
        
        :param agent: User agent for GET requests
        :param url: RSS feed URL
        """
        self.url = url
        self.agent = agent
        
        self.read_rss()
    
    def read_rss(self) -> List[dict]:
        """
        Scrape RSS feeds
        
        :param ids: List of IDs to mark as posted
        :param max_tracked_ids: Maximum number of IDs to keep track of
        """
        d = feedparser.parse(
            self.url,
            request_headers = {
                'User-agent': self.agent
            }
        )
        return d.entries