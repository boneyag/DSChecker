# Author: Francisco Ribeiro (original)
#         Akalanka Galappaththi (modified)
from dschecker.clients.openai_client import OpenAIClient
from dschecker.clients.togetherai_client import TogetherAIClient

CLIENTS = {
    "gpt-3.5-turbo": OpenAIClient,
    "gpt-3.5-turbo-0125": OpenAIClient,
    "gpt-4o": OpenAIClient,
    "gpt-4o-2024-05-13": OpenAIClient,
    "gpt-4o-mini": OpenAIClient,
    "gpt-4o-mini-2024-07-18": OpenAIClient,
    "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo": TogetherAIClient,
}


class Model:
    def __init__(self, model_name):
        self.model_name = model_name
        self.client = CLIENTS[model_name]()

    def generate(self, messages, temperature, tools, tool_choice):
        response = self.client.mk_request(
            self.model_name,
            messages,
            temperature=temperature,
            tools=tools,
            tool_choice=tool_choice,
        )

        return response
