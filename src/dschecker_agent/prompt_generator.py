import os

from dschecker.logging_util.logger import setup_logger
from dschecker_agent.templates.template import Base


logger = setup_logger(__name__)


def generate_prompt(**kwargs):
    template = Base(**kwargs)

    header_path = os.path.join(
        os.path.dirname(__file__), "templates/resources", "header.txt"
    )
    with open(header_path, "r") as header_file:
        header = header_file.read()

    return "\n\n".join([header, template.get_text()])
