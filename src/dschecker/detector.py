import argparse
import json
import os

from dschecker.logging_util.logger import setup_logger
from dschecker.models.models import Model
from dschecker.prompt_generator import generate_prompt
from dschecker.utils.prompt_helper import add_line_numbers_to_code

logger = setup_logger(__name__)

THIS_PATH = os.path.dirname(__file__)


def detect_misuses(
    model,
    prompt_style,
    example_type,
    prompt_mode,
    input_data,
    repeats,
    instance_num,
    output,
):
    """
    Keyword arguments:
    model -- LLM's name (e.g., gpt-4o for current model or gpt-4o-2024-05-13 for especific version)
    prompt_style -- zero-shot or few-shot
    example_type -- static or tailored, only used when the prompt_style is few-shot
    prompt_mode -- base, dtype, directive, or full: this determin the information composition of the prompt
    input_data -- a JSON object with misuse data
    repeats -- number of times a prompt should be repeated to LLM
    instance_num -- provide string instance num (should match with keys in the JSON object) if the LLM should only run for a specific instance
    output -- folder name to store results/responses of LLM
    """
    # setup results directories (i.e., prompts and responses)
    sub_dir_name = (
        prompt_mode
        if prompt_style == "zero-shot"
        else f"{prompt_style}_{example_type}_{prompt_mode}"
    )  # need to updated subdir name for few-shot
    os.makedirs(
        os.path.join(THIS_PATH, "../results", output, "prompts", sub_dir_name),
        exist_ok=True,
    )
    os.makedirs(
        os.path.join(THIS_PATH, "../results", output, "responses", sub_dir_name),
        exist_ok=True,
    )

    if instance_num:
        detect_a_misuse(
            model=model,
            prompt_style=prompt_style,
            example_type=example_type,
            prompt_mode=prompt_mode,
            repeats=repeats,
            instance=input_data[instance_num],
            output=output,
        )
    else:
        for misuse_key in input_data.keys():
            detect_a_misuse(
                model=model,
                prompt_style=prompt_style,
                example_type=example_type,
                prompt_mode=prompt_mode,
                repeats=repeats,
                instance=input_data[misuse_key],
                output=output,
            )


def detect_a_misuse(
    model, prompt_style, example_type, prompt_mode, repeats, instance, output
):
    if os.path.exists(
        os.path.join(THIS_PATH, "../data", instance["code_file_rel_path"])
    ):
        with open(
            os.path.join(THIS_PATH, "../data", instance["code_file_rel_path"])
        ) as f:
            code_snippet = f.read()
            code_snippet_with_line_nums = "\n".join(
                add_line_numbers_to_code(code_snippet)
            )
    else:
        raise OSError(f"{instance['code_file_rel_path']} does not exist.")

    # determine directive type based on the content
    if instance["directive"]["parameter"] != "":
        directive_type = "param"
    elif instance["directive"]["api"] != "":
        directive_type = "api"
    else:
        directive_type = "other"

    # determine if there sample should be included or not
    add_sample = True if instance["api_misuse"]["data"]["sample"] != "" else False

    prompt = generate_prompt(
        prompt_style,
        example_type,
        prompt_mode,
        lib=instance["lib"],
        code=code_snippet_with_line_nums,
        directive_type=directive_type,
        directive=instance["directive"]["explicit_directive"],
        api=instance["directive"]["api"],
        parameter=instance["directive"]["parameter"],
        add_sample=add_sample,
        variable=instance["api_misuse"]["data"]["variable_name"],
        linenum=instance["api_misuse"]["data"]["variable_line_num"],
        type=instance["api_misuse"]["data"]["type"],
        additional=instance["api_misuse"]["data"]["additional_info"],
        sample=instance["api_misuse"]["data"]["sample"],
        misuse_instance=instance["similar_instances"]["misuse_instance"],
        correct_instance=instance["similar_instances"]["correct_instance"],
    )

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that helps to detect and fix issues related to API of Python data science libraries in given code snippets. Detecting issues does not include minor issues such as types, formatting, or style.",
        }
    ]
    messages.append({"role": "user", "content": prompt})
    # logger.info(messages)

    model = Model(model_name=model)

    if repeats == 1:
        llm_output = model.generate(
            messages=messages, temperature=0.0, tools=None, tool_choice=None
        )

        llm_output_json = json.loads(llm_output.model_dump_json(indent=4))
        response = llm_output_json["choices"][0]["message"]["content"]

        logger.info(response)

        # report that contain a summary of misuse info and prompt, response file paths
        report = {
            "num": instance["num"],
            "source": instance["source"],
            "lib": instance["lib"],
            "lib_version": instance["lib_version"],
            "code_file_path": instance["code_file_rel_path"],
        }

        prompt_mode = (
            prompt_mode
            if prompt_style == "zero-shot"
            else f"{prompt_style}_{example_type}_{prompt_mode}"
        )
        write_files(
            prompt_mode=prompt_mode,
            prompt=messages[1]["content"],
            instance=instance["num"],
            response=response,
            output=output,
        )

        report["prompt_file_path"] = (
            f"results/{output}/prompts/{prompt_mode}/{instance['num']}.txt"
        )
        report["response_file_path"] = (
            f"results/{output}/responses/{prompt_mode}/{instance['num']}.json"
        )

        write_or_update_report(prompt_mode=prompt_mode, report=report, output=output)
    else:
        # report that contain a summary of misuse info and prompt, response file paths
        report = {
            "num": instance["num"],
            "source": instance["source"],
            "lib": instance["lib"],
            "lib_version": instance["lib_version"],
            "code_file_path": instance["code_file_rel_path"],
        }

        for i in range(1, repeats + 1):
            llm_output = model.generate(
                messages=messages, temperature=0.0, tools=None, tool_choice=None
            )

            llm_output_json = json.loads(llm_output.model_dump_json(indent=4))
            response = llm_output_json["choices"][0]["message"]["content"]

            logger.info(response)
            prompt_mode = (
                prompt_mode
                if prompt_style == "zero-shot"
                else f"{prompt_style}_{example_type}_{prompt_mode}"
            )
            write_files(
                prompt_mode=prompt_mode,
                prompt=messages[1]["content"],
                instance=instance["num"],
                response=response,
                output=output,
                repeat_i=i,
            )

        report["prompt_file_path"] = (
            f"results/{output}/prompts/{prompt_mode}/{instance['num']}.txt"
        )
        report["response_file_path"] = []
        for i in range(1, repeats + 1):
            report["response_file_path"].append(
                f"results/{output}/responses/{prompt_mode}/{instance['num']}_{i}.json"
            )

        write_or_update_report(prompt_mode=prompt_mode, report=report, output=output)


def write_files(prompt_mode, prompt, instance, response, output, repeat_i=0):
    PROMPT_PATH = os.path.join(THIS_PATH, "../results", output, "prompts")
    RESPONSE_PATH = os.path.join(THIS_PATH, "../results", output, "responses")

    with open(os.path.join(PROMPT_PATH, f"{prompt_mode}", f"{instance}.txt"), "w") as f:
        f.write(prompt)
    if repeat_i == 0:
        with open(
            os.path.join(RESPONSE_PATH, f"{prompt_mode}", f"{instance}.json"), "w"
        ) as f:
            json.dump(response, f, indent=4)
    else:
        with open(
            os.path.join(
                RESPONSE_PATH, f"{prompt_mode}", f"{instance}_{repeat_i}.json"
            ),
            "w",
        ) as f:
            json.dump(response, f, indent=4)
    logger.info(f"Files written for instance {instance} in {output}")


def write_or_update_report(prompt_mode, report, output):
    if not os.path.exists(
        os.path.join(THIS_PATH, "../results", output, f"report_{prompt_mode}.json")
    ):
        with open(
            os.path.join(THIS_PATH, "../results", output, f"report_{prompt_mode}.json"),
            "w",
        ) as f:
            reports = {}
            reports[report["num"]] = report
            json.dump(reports, f, indent=4)
    else:
        with open(
            os.path.join(THIS_PATH, "../results", output, f"report_{prompt_mode}.json"),
            "r",
        ) as f:
            reports = json.load(f)
        reports[report["num"]] = report
        with open(
            os.path.join(THIS_PATH, "../results", output, f"report_{prompt_mode}.json"),
            "w",
        ) as f:
            json.dump(reports, f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="DSChecker",
        description="Run the detector/fixer for Python data science libraries.",
    )

    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="gpt-4o-mini-2024-07-18",
        choices=[
            "gpt-4o-mini-2024-07-18",
            "gpt-4o-2024-05-13",
            "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        ],
    )
    parser.add_argument(
        "-s",
        "--style",
        type=str,
        default="zero-shot",
        choices=["zero-shot", "few-shot"],
    )
    parser.add_argument(
        "-p",
        "--prompt",
        type=str,
        default="base",
        choices=["base", "directive", "dtype", "full"],
    )
    parser.add_argument(
        "-e",
        "--example-type",
        type=str,
        default="static",
        choices=["static", "tailored"],
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        required=True,
        help="Input data file in JSON format. Must be in the data directory.",
    )
    parser.add_argument(
        "-r",
        "--repeat",
        type=int,
        default=1,
        help="Number of times to repeat the prompt",
    )
    parser.add_argument(
        "-i",
        "--instance",
        type=str,
        help="Only if you need to run the experiment for a single misuse. Should match for a key in the input JSON data",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="Name of the directory to save prompts and responses. Will be created in the results directory.",
    )

    args = parser.parse_args()

    input_file = os.path.join(THIS_PATH, "../data", args.file)
    if not os.path.exists(input_file):
        raise IOError(f"Input file {args.file} does not exist.")
    else:
        with open(input_file) as f:
            misuse_data = json.load(f)

    detect_misuses(
        model=args.model,
        prompt_style=args.style,
        prompt_mode=args.prompt,
        example_type=args.example_type,
        input_data=misuse_data,
        repeats=args.repeat,
        instance_num=args.instance,
        output=args.output,
    )
