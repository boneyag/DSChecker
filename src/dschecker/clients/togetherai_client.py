# Author: Akalanka Galappaththi (adapted from original)
import os

from dschecker.clients.client import Client


class TogetherAIClient(Client):
    def __init__(self):
        super().__init__(
            api_key=os.environ.get("TOGETHER_API_KEY"),
            base_url="https://api.together.xyz/v1",
        )
