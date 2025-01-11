import json
import os
import logging
from typing import List, Set
from dotenv import load_dotenv
from pyfacebook import GraphAPI
import feedparser
from urllib.parse import urlparse, urlunparse
from requests.models import PreparedRequest
from datetime import datetime, timedelta
import time

logging.basicConfig(level=logging.INFO)

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
                logging.info(f"Created new tracking file: {self.tracking_file}")
            
            # Read existing posted IDs
            with open(self.tracking_file, 'r') as f:
                logging.info(f"Loaded posted IDs from {self.tracking_file}")
                return set(json.load(f))
        
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error loading posted IDs: {e}")
            return set()
    
    def _save_posted_ids(self):
        """
        Save posted IDs to file.
        """
        try:
            with open(self.tracking_file, 'w') as f:
                json.dump(list(self.posted_ids), f)
            logging.info(f"Saved posted IDs to {self.tracking_file}")
        except IOError as e:
            logging.error(f"Error saving posted IDs: {e}")
    
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
        
        self.queue = self._construct_queue()
     
    def _construct_queue(self) -> List[float]:
        """
        Create queue for Facebook posting
        
        :return: List of slots for posts
        """
        now = datetime.now()
        max_time = now + timedelta(hours=24)
        
        if self.posts_per_day == 1:
            slot_time = now.replace(hour=self.day_start, minute=0, second=0, microsecond=0)
            if slot_time < now:
                slot_time += timedelta(days=1)
            if slot_time > max_time:
                slot_time = max_time
            logging.info(f"Constructed queue with one slot at {slot_time}")
            return [int(slot_time.timestamp())]
        
        n = (self.day_end - self.day_start) / (self.posts_per_day - 1)
        slots = []
        for i in range(self.posts_per_day):
            slot_time = now.replace(hour=self.day_start, minute=0, second=0, microsecond=0) + timedelta(hours=i * n)
            if slot_time < now:
                slot_time += timedelta(days=1)
            if slot_time > max_time:
                slot_time = max_time
            slots.append(int(slot_time.timestamp()))
        
        logging.info(f"Constructed queue with slots: {slots}")
        return slots

class FacebookPoster():
    def __init__(self, page_id: str, post_type: str, kicker: str):
        """
        Initialize Facebook Poster
        
        :param page_id: Target Facebook page ID
        :param queue: Queue settings from create_queue method
        """
        self.page_id = page_id
        self.kicker = kicker
        self.fb = self._auth_facebook()
        
        if post_type not in ["image", "link"]:
            raise ValueError("Invalid post type. Choose 'image' or 'link'")
        else:
            self.post_type = post_type
        
    def _auth_facebook(self) -> GraphAPI:

        load_dotenv()
        app_id = os.getenv("APP_ID")
        app_secret = os.getenv("APP_SECRET")
        access_token=os.getenv("ACCESS_TOKEN")
        
        if not app_id or not app_secret or not access_token:
            raise ValueError("Missing Facebook credentials. Check .env file.")

        fb = GraphAPI(app_id, app_secret, access_token)
        
        return fb
    
    def _strip_url(self, url: str) -> str:
        """
        Remove query parameters from URL
        
        :param url: URL to be stripped
        :return: URL without query parameters
        """
        parsed_url = urlparse(url)
        return urlunparse(parsed_url._replace(query=""))
    
    def _format_message(self, item: dict) -> str:
        """
        Format message for Facebook post
        
        :param item: Feed item
        :return: Formatted message
        """
        kicker = self.kicker
        title = item.title.strip("'()")
        link = item.link.strip("'()")
        summary = item.summary
        
        return f"{title}\n\n{summary}\n\n{kicker} {link}"
    
    def send_posts(self, slots: List, unposted_items: List[dict]):
        """
        :param slots: List of slots for posts
        """
        page_id = self.page_id
        fb = self.fb
        post_type = self.post_type
        
        for item in unposted_items:
            if slots:
                slot = slots.pop(0)
            else:
                logging.warning("No more slots available within 24 hours")
                break
                
            caption = self._format_message(item)
            
            # Post with media
            if post_type == "image": 
                media_url = self._strip_url(item.media_content[0]['url'])
                logging.info(f"Scheduling image post: {item.title} at {slot}")
                data = fb.post_object(
                    object_id = page_id,
                    data = {
                        'caption': caption,
                        'url': media_url,
                        'published': "false",
                        'scheduled_publish_time': slot
                    },
                    connection = "photos"
                )
                logging.info(f"Scheduled '{item.title}' with ID {data['id']}")
            if post_type == "link":
                logging.info(f"Scheduling link post: {item.title} at {slot}")
                fb.post_object(
                    object_id = page_id,
                    data = {
                        'message': self._format_message(item),
                        'link': item.link,
                        'published': "true",
                    },
                    connection = "feed"
                )

class FeedScraper:
    def __init__(self, url: str, agent: str, params: dict):
        """
        Initialize FeedScraper instance
        
        :param agent: User agent for HTTP requests
        :param url: RSS feed URL
        """
        self.url = self._create_url(url, params)
        self.agent = agent
        self.entries = self._read_rss()
    
    def _create_url(self, url: str, params: dict) -> str:
        """
        Create URL with query parameters
        
        :param base: Base URL
        :param params: Query parameters
        :return: URL with query parameters
        """
        req = PreparedRequest()
        req.prepare_url(url, params)
        logging.info(f"Created URL: {req.url}")
        
        return req.url
    def _read_rss(self) -> List[dict]:
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
        logging.info(f"Found {len(d.entries)} feed entries")
        return d.entries