# Author: Francisco Ribeiro (original)
#         Akalanka Galappaththi (modified)
from abc import ABC

from openai import OpenAI

from dschecker.logging_util.logger import setup_logger

logger = setup_logger(__name__)


class Client(ABC):
    def __init__(self, api_key, base_url=None):
        self.client = (
            OpenAI(api_key=api_key)
            if base_url is None
            else OpenAI(api_key=api_key, base_url=base_url)
        )

    def mk_request(self, model_name, messages, temperature, tools, tool_choice):
        completion = self.client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            tools=tools,
            tool_choice=tool_choice,
            response_format={"type": "json_object"},
        )
        logger.info(f"Total # of tokens: {completion.usage.total_tokens}")

        return completion
