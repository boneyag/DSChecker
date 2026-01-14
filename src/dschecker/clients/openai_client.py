# Author: Francisco Ribeiro (original)
#         Akalanka Galappaththi (modified)
import os

from dschecker.clients.client import Client


class OpenAIClient(Client):
    def __init__(self):
        super().__init__(api_key=os.environ.get("OPENAI_API_KEY"))
