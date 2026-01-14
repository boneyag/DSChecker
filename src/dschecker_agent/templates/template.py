from abc import ABC, abstractmethod
from string import Template
import os


class Prompt(ABC):
    @abstractmethod
    def get_text(self):
        pass


class Base(Prompt):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.task = _read_file("task")
        self.response = _read_file("response")
        self.template_parts = [self.task, self.response]
        self.template = Template("\n\n".join(self.template_parts))

    def get_text(self):
        return self.template.safe_substitute(self.kwargs)


def _read_file(file: str):
    if file == "task":
        with open(os.path.join(os.path.dirname(__file__), "resources/task.txt")) as f:
            data = f.read()
        return data
    if file == "response":
        with open(
            os.path.join(os.path.dirname(__file__), "resources/response.txt")
        ) as f:
            data = f.read()
        return data
