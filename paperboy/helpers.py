import json
import os
from typing import List, Set

class PostTracker:
    def __init__(self, tracking_file: str = 'posted_ids.json'):
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
#something goes here
    def post_to_facebook(self, post):
        """
        something will go here
        """