import json
import os
from abc import ABC, abstractmethod
from string import Template

from dschecker.utils.prompt_helper import add_line_numbers_to_code


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


class Directive(Base):
    def __init__(self, **kwargs):
        Base.__init__(self, **kwargs)

        if kwargs["directive"] != "":
            self.directive = _read_file(kwargs["directive_type"])

        self.template_parts = [self.task, self.response]
        if hasattr(self, "directive"):
            self.template_parts.insert(1, self.directive)
        self.template = Template("\n\n".join(self.template_parts))


class Dtype(Base):
    def __init__(self, **kwargs):
        Base.__init__(self, **kwargs)
        self.data = _read_file("data") if kwargs["add_sample"] else _read_file("type")
        self.template_parts = [self.task, self.data, self.response]
        self.template = Template("\n\n".join(self.template_parts))


class Full(Dtype, Directive):
    def __init__(self, **kwargs):
        Base.__init__(self, **kwargs)
        Dtype.__init__(self, **kwargs)
        Directive.__init__(self, **kwargs)

        self.template_parts = [self.task, self.data, self.response]
        if hasattr(self, "directive"):
            self.template_parts.insert(1, self.directive)
        self.template = Template("\n\n".join(self.template_parts))


# This could be an overkill, but this is the only way I found to dynamically create few-shot prompts
# ref [Dynamic inheritance in Python](https://stackoverflow.com/questions/21060073/dynamic-inheritance-in-python)
def get_dynamic_fewshot_static_class(super_class):
    class FewshotStatic(super_class):
        def __init__(self, **kwargs):
            super_class.__init__(self, **kwargs)

            self.prefix = _read_file("prefix")
            self.suffix = _read_file("suffix")

            self.examples = _read_file("ex")
            # example 1
            ex1_instance = self.examples["non-dl-misuse"]
            with open(
                os.path.join(
                    os.path.dirname(__file__), ex1_instance["code_file_rel_path"]
                )
            ) as f:
                code = f.read()
            ex1_kwargs = {
                "lib": ex1_instance["lib"],
                "code": "\n".join(add_line_numbers_to_code(code)),
                "directive_type": "param",
                "directive": ex1_instance["directive"]["explicit_directive"],
                "api": ex1_instance["directive"]["api"],
                "parameter": ex1_instance["directive"]["parameter"],
                "add_sample": (
                    True
                    if ex1_instance["api_misuse"]["data"]["sample"] != ""
                    else False
                ),
                "variable": ex1_instance["api_misuse"]["data"]["variable_name"],
                "linenum": ex1_instance["api_misuse"]["data"]["variable_line_num"],
                "type": ex1_instance["api_misuse"]["data"]["type"],
                "additional": ex1_instance["api_misuse"]["data"]["additional_info"],
                "sample": ex1_instance["api_misuse"]["data"]["sample"],
            }
            ex1 = super_class(
                **ex1_kwargs
            )  # create example1 based on the same zero-shot prompt
            self.ex1_prompt = ex1.get_text()
            with open(
                os.path.join(
                    os.path.dirname(__file__), ex1_instance["patch_file_rel_path"]
                )
            ) as f:
                patch = f.read()
            self.ex1_response = json.dumps(
                {
                    "correct": "no",
                    "explanation": ex1_instance["api_misuse"]["explanation"],
                    "patch": patch,
                }
            )
            # example 2
            ex2_instance = self.examples["non-dl-correct"]
            with open(
                os.path.join(
                    os.path.dirname(__file__), ex2_instance["code_file_rel_path"]
                )
            ) as f:
                code = f.read()
            ex2_kwargs = {
                "lib": ex2_instance["lib"],
                "code": "\n".join(add_line_numbers_to_code(code)),
                "directive_type": "param",
                "directive": ex2_instance["directive"]["explicit_directive"],
                "api": ex2_instance["directive"]["api"],
                "parameter": ex2_instance["directive"]["parameter"],
                "add_sample": (
                    True
                    if ex2_instance["api_misuse"]["data"]["sample"] != ""
                    else False
                ),
                "variable": ex2_instance["api_misuse"]["data"]["variable_name"],
                "linenum": ex2_instance["api_misuse"]["data"]["variable_line_num"],
                "type": ex2_instance["api_misuse"]["data"]["type"],
                "additional": ex2_instance["api_misuse"]["data"]["additional_info"],
                "sample": ex2_instance["api_misuse"]["data"]["sample"],
            }
            ex2 = super_class(**ex2_kwargs)
            self.ex2_prompt = ex2.get_text()
            self.ex2_response = json.dumps({"correct": "yes"})

            self.template_parts = [
                self.prefix,
                "Example 1:",
                self.ex1_prompt,
                self.ex1_response,
                "Example 2:",
                self.ex2_prompt,
                self.ex2_response,
                self.suffix,
                self.task,
                self.response,
            ]
            if hasattr(self, "data"):
                self.template_parts.insert(8, self.data)
            if hasattr(self, "directive"):
                self.template_parts.insert(8, self.directive)
            self.template = Template("\n\n".join(self.template_parts))

    return FewshotStatic


def get_dynamic_fewshot_tailored_class(super_class):
    class FewshotTailored(super_class):
        def __init__(self, **kwargs):
            super_class.__init__(self, **kwargs)

            self.prefix = _read_file("prefix")
            self.suffix = _read_file("suffix")

            # need to access to API_misuses.json and code_snippets to generate examples
            with open(
                os.path.join(os.path.dirname(__file__), "../../data/API_misuses.json")
            ) as f:
                data = json.load(f)
            # example 1
            ex1_instance = data[kwargs["misuse_instance"]]
            with open(
                os.path.join(
                    os.path.dirname(__file__),
                    "../../data",
                    ex1_instance["code_file_rel_path"],
                )
            ) as f:
                code = f.read()
            if ex1_instance["directive"]["parameter"] != "":
                directive_type = "param"
            elif ex1_instance["directive"]["api"] != "":
                directive_type = "api"
            else:
                directive_type = "other"
            ex1_kwargs = {
                "lib": ex1_instance["lib"],
                "code": "\n".join(add_line_numbers_to_code(code)),
                "directive_type": directive_type,
                "directive": ex1_instance["directive"]["explicit_directive"],
                "api": ex1_instance["directive"]["api"],
                "parameter": ex1_instance["directive"]["parameter"],
                "add_sample": (
                    True
                    if ex1_instance["api_misuse"]["data"]["sample"] != ""
                    else False
                ),
                "variable": ex1_instance["api_misuse"]["data"]["variable_name"],
                "linenum": ex1_instance["api_misuse"]["data"]["variable_line_num"],
                "type": ex1_instance["api_misuse"]["data"]["type"],
                "additional": ex1_instance["api_misuse"]["data"]["additional_info"],
                "sample": ex1_instance["api_misuse"]["data"]["sample"],
            }
            ex1 = super_class(**ex1_kwargs)
            self.ex1_prompt = ex1.get_text()
            # read the patch in data dir
            with open(
                os.path.join(
                    os.path.dirname(__file__),
                    "../../data",
                    ex1_instance["patch_file_rel_path"],
                )
            ) as f:
                patch = f.read()
            self.ex1_response = json.dumps(
                {
                    "correct": "no",
                    "explanation": ex1_instance["api_misuse"]["explanation"],
                    "patch": patch,
                }
            )

            # example 2
            ex2_instance = data[kwargs["correct_instance"]]
            with open(
                os.path.join(
                    os.path.dirname(__file__),
                    "../../data",
                    ex2_instance["code_file_rel_path"],
                )
            ) as f:
                code = f.read()
            if ex2_instance["directive"]["parameter"] != "":
                directive_type = "param"
            elif ex2_instance["directive"]["api"] != "":
                directive_type = "api"
            else:
                directive_type = "other"
            ex2_kwargs = {
                "lib": ex2_instance["lib"],
                "code": "\n".join(add_line_numbers_to_code(code)),
                "directive_type": directive_type,
                "directive": ex2_instance["directive"]["explicit_directive"],
                "api": ex2_instance["directive"]["api"],
                "parameter": ex2_instance["directive"]["parameter"],
                "add_sample": (
                    True
                    if ex2_instance["api_misuse"]["data"]["sample"] != ""
                    else False
                ),
                "variable": ex2_instance["api_misuse"]["data"]["variable_name"],
                "linenum": ex2_instance["api_misuse"]["data"]["variable_line_num"],
                "type": ex2_instance["api_misuse"]["data"]["type"],
                "additional": ex2_instance["api_misuse"]["data"]["additional_info"],
                "sample": ex2_instance["api_misuse"]["data"]["sample"],
            }
            ex2 = super_class(**ex2_kwargs)
            self.ex2_prompt = ex2.get_text()
            self.ex2_response = json.dumps({"correct": "yes"})

            self.template_parts = [
                self.prefix,
                "Example 1:",
                self.ex1_prompt,
                self.ex1_response,
                "Example 2:",
                self.ex2_prompt,
                self.ex2_response,
                self.suffix,
                self.task,
                self.response,
            ]
            if hasattr(self, "data"):
                self.template_parts.insert(8, self.data)
            if hasattr(self, "directive"):
                self.template_parts.insert(8, self.directive)
            self.template = Template("\n\n".join(self.template_parts))

    return FewshotTailored


def _read_file(file: str):
    if file == "task":
        with open(os.path.join(os.path.dirname(__file__), "resources/task.txt")) as f:
            data = f.read()
        return data
    elif file == "response":
        with open(
            os.path.join(os.path.dirname(__file__), "resources/response.txt")
        ) as f:
            data = f.read()
        return data
    elif file == "api":
        with open(
            os.path.join(os.path.dirname(__file__), "resources/directive_api.txt")
        ) as f:
            data = f.read()
        return data
    elif file == "param":
        with open(
            os.path.join(os.path.dirname(__file__), "resources/directive_param.txt")
        ) as f:
            data = f.read()
        return data
    elif file == "other":
        with open(
            os.path.join(os.path.dirname(__file__), "resources/directive_other.txt")
        ) as f:
            data = f.read()
        return data
    elif file == "data":
        with open(
            os.path.join(os.path.dirname(__file__), "resources/data_type_sample.txt")
        ) as f:
            data = f.read()
        return data
    elif file == "type":
        with open(
            os.path.join(os.path.dirname(__file__), "resources/data_type.txt")
        ) as f:
            data = f.read()
        return data
    elif file == "prefix":
        with open(
            os.path.join(os.path.dirname(__file__), "resources/few_shot_prefix.txt")
        ) as f:
            data = f.read()
        return data
    elif file == "suffix":
        with open(
            os.path.join(os.path.dirname(__file__), "resources/few_shot_suffix.txt")
        ) as f:
            data = f.read()
        return data
    elif file == "ex":
        with open(
            os.path.join(os.path.dirname(__file__), "resources/examples.json")
        ) as f:
            data = json.load(f)
        return data
