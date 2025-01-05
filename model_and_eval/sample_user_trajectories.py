"""
Given a product, this script returns a list of k related products that users have also interacted with.
"""

from huggingface_hub import hf_hub_download
import json
from random import sample
from utils import asin2product


class UserTrajectories:
    def __init__(self) -> None:
        self.user2asin = {}

    def download(self, cache_dir) -> None:
        """downloads the user2asin.json file"""
        file_path = hf_hub_download(
            repo_id="randomath/Amazon-combined",
            filename="user2asin.json",
            repo_type="dataset",
            local_dir=cache_dir,
        )
        with open(file_path) as f:
            self.user2asin = json.load(f)

    def _get_users(self, product_entry: dict) -> list[str]:
        """returns the list of users that have interacted with the product"""
        users = []
        for review in product_entry["reviews"]:
            users.append(review["user_id"])
        return users

    def get_user_interactions(self, product_entry: dict, k: int) -> list[str]:
        """returns a list of k related products that users have interacted with"""
        users = self._get_users(product_entry)
        asins = [
            self.user2asin[user] for user in users if len(self.user2asin[user]) >= 3
        ]
        if len(asins) <= k:
            return asins
        return sample(asins, k)

    def sample_user_interactions(self, product_entry: dict, k: int = 1) -> list[str]:
        """returns a list of k product names that users have interacted with"""
        trajectories = self.get_user_interactions(product_entry, k)
        return [
            [asin2product(asin) for asin in trajectory] for trajectory in trajectories
        ]
