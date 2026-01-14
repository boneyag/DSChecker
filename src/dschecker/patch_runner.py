import argparse
import ast
import json
import os
import subprocess

from dschecker.logging_util.logger import setup_logger

logger = setup_logger(__name__, level="debug")


def apply_patch(buggy_file, patch_file, output_file_name):
    try:
        patch_process = subprocess.Popen(
            [
                "patch",
                buggy_file,
                "--input",
                patch_file,
                "--ignore-whitespace",
                "--normal",
                "--output",
                output_file_name,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        out, err = patch_process.communicate(timeout=10)
        if patch_process.returncode == 0:
            print("Patch applied successfully.")
            logger.info(out)
            logger.debug(err)
        else:
            print("Patch failed.")
            logger.info(out)
            logger.debug(err)
    except subprocess.TimeoutExpired:
        patch_process.kill()
        out, err = patch_process.communicate()
        logger.info(out)
        logger.debug(err)


def patch_misuses(fix_path, res_dir, response_path, report_name, instance_num, rep_num):
    with open(
        os.path.join(os.path.dirname(__file__), "../results", res_dir, report_name)
    ) as f:
        report = json.load(f)

    if instance_num:
        if instance_num not in report:
            raise ValueError(f"{instance_num} is not a instance number")
        patch_a_misuse(report[instance_num], rep_num, fix_path, response_path)
    else:
        # TODO
        # patch_all_misuses() -- this does not exist
        pass


def patch_a_misuse(code_snippet, rep_num, fix_path, response_path):
    source_file = os.path.join(
        os.path.dirname(__file__), "../data", code_snippet["code_file_path"]
    )
    if os.path.exists(source_file):
        logger.info(f"source file for item {code_snippet['num']} exist")

    if isinstance(code_snippet["response_file_path"], list) and rep_num:
        # rep_num - 1 to align index
        response_file_name = code_snippet["response_file_path"][rep_num - 1].split("/")[
            -1
        ]
        with open(os.path.join(response_path, response_file_name)) as rf:
            response = json.load(rf)
        response = ast.literal_eval(
            response
        )  # workaround -- json.load return str instead of dict
        patch_text = response["patch"]

        # create a patch file and fix file
        patch_file = os.path.join(
            fix_path, f"{code_snippet['num']}_{rep_num}_patch.txt"
        )
        with open(patch_file, "w") as wf:
            wf.write(patch_text + "\n")
            logger.info("Create a patch file")
        fix_file = os.path.join(fix_path, f"{code_snippet['num']}_{rep_num}_patched.py")

        apply_patch(source_file, patch_file, fix_file)

    elif isinstance(
        code_snippet["response_file_path"], list
    ):  # run all patches when not similar
        for i, res_path in enumerate(code_snippet["response_file_path"]):
            response_file_name = res_path.split("/")[-1]
            with open(os.path.join(response_path, response_file_name)) as rf:
                response = json.load(rf)

            # workaround -- json.load return str instead of dict
            response = ast.literal_eval(response)
            if "patch" not in response or response["patch"] == "":
                logger.info("Did not generate a patch")
                continue
            patch_text = response["patch"]

            # create a patch file and fix file
            patch_file = os.path.join(
                fix_path, f"{code_snippet['num']}_{i + 1}_patch.txt"
            )
            with open(patch_file, "w") as wf:
                wf.write(patch_text + "\n")
                logger.info("Create a patch file")
            fix_file = os.path.join(
                fix_path, f"{code_snippet['num']}_{i + 1}_patched.py"
            )

            apply_patch(source_file, patch_file, fix_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Apply LLM generated patches to misuses"
    )

    parser.add_argument(
        "-d",
        "--results-directory",
        type=str,
        required=True,
        help=(
            "Directory name of LLM generated responses stored in "
            "(should be in the results directory)"
        ),
    )
    parser.add_argument(
        "-s",
        "--prompt-style",
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
        "-e", "--example-type", type=str, choices=["static", "tailored"]
    )
    parser.add_argument(
        "-i",
        "--instance",
        type=str,
        help="Code snippet's number (to apply the patch)",
    )
    parser.add_argument(
        "-r",
        "--repetition",
        type=int,
        help=("This is only required if one code snippet prompted multipletimes"),
    )

    args = parser.parse_args()
    res_dir_path = os.path.join(
        os.path.dirname(__file__), "../results", args.results_directory
    )
    if not os.path.exists(res_dir_path):
        raise FileNotFoundError(
            f"Results directory {args.results_directory} does not exits"
        )

    if args.prompt_style == "few-shot" and args.example_type is None:
        raise ValueError("--example-type cannot be None for few-shot prompts")

    if args.prompt_style == "zero-shot":
        response_path = os.path.join(res_dir_path, "responses", args.prompt)
        fix_dir_path = os.path.join(res_dir_path, "bug_fixes", args.prompt)
        report_name = f"report_{args.prompt}.json"
    else:
        response_path = os.path.join(
            res_dir_path, "responses", f"few-shot_{args.example_type}_{args.prompt}"
        )
        fix_dir_path = os.path.join(
            res_dir_path, "bug_fixes", f"few-shot_{args.example_type}_{args.prompt}"
        )
        report_name = (
            f"report_{args.prompt_style}_{args.example_type}_{args.prompt}.json"
        )

    if not os.path.exists(response_path):
        raise FileNotFoundError(f"Directory {response_path} does not exist.")

    # create a directory to store patches
    os.makedirs(fix_dir_path, exist_ok=True)

    patch_misuses(
        fix_dir_path,
        args.results_directory,
        response_path,
        report_name,
        args.instance,
        args.repetition,
    )
