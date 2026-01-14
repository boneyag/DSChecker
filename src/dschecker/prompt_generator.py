import os

from dschecker.logging_util.logger import setup_logger
from dschecker.templates.template import (
    Base,
    Directive,
    Dtype,
    Full,
    get_dynamic_fewshot_static_class,
    get_dynamic_fewshot_tailored_class,
)

logger = setup_logger(__name__)

template_class_mapping = {
    "base": Base,
    "dtype": Dtype,
    "directive": Directive,
    "full": Full,
}


def generate_prompt(template_style, example_type, template_type, **kwargs):
    """
    Generate a prompt based on the template type and domain.

    Args:
        template_style (str): The style of the template (zero-shot or few-shot)
        example_type (str): The type examples to be included in few-shot template/prompt
        template_type (str): The type of template to use (e.g., Base, Directive).
        **kwargs: Additional arguments to substitute placeholders in template.

    Returns:
        str: The generated prompt.
    """
    logger.info(f"Generating a {template_type} prompt")
    if template_style == "zero-shot":
        template = template_class_mapping[template_type](**kwargs)
    elif template_style == "few-shot":
        if example_type == "static":
            # first get the dynamically inherited class
            fewshot_stat_cls = get_dynamic_fewshot_static_class(
                template_class_mapping[template_type]
            )
            template = fewshot_stat_cls(**kwargs)
        elif example_type == "tailored":
            fewshot_tailored_cls = get_dynamic_fewshot_tailored_class(
                template_class_mapping[template_type]
            )
            template = fewshot_tailored_cls(**kwargs)

    # header is common for all promts and has no placeholders
    header_path = os.path.join(
        os.path.dirname(__file__), "templates/resources", "header.txt"
    )
    with open(header_path, "r") as header_file:
        header = header_file.read()

    return header + "\n\n" + template.get_text()
