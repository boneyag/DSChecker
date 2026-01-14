import argparse
import ast
import json
import os

import numpy as np
import pandas as pd

from dschecker.logging_util.logger import setup_logger
from dschecker.utils.response_similarity_calculator import get_cosine_similarity

logger = setup_logger(__name__)


def generate_detection_results_report(data_file, results_path, response_dir_name):
    with open(data_file) as f:
        data = json.load(f)

    with open(os.path.join(results_path, f"report_{response_dir_name}.json")) as f:
        results = json.load(f)

    rows = []
    for k, v in results.items():
        ground_truth = data[k]["correct"]
        row = {}
        row["num"] = k
        responses = []
        for i, res_report_path in enumerate(v["response_file_path"]):
            with open(os.path.join("../", res_report_path), "r") as f:
                json_string = json.load(f)
            res_object = ast.literal_eval(
                json_string
            )  # workaround -- json.load return str instead of dict
            responses.append(json_string)  # to get similarity scores between responses
            # logger.info(res_object["correct"])
            if ground_truth == res_object["correct"] == "no":
                row[f"r{i + 1}"] = "TP"
            if ground_truth == res_object["correct"] == "yes":
                row[f"r{i + 1}"] = "TN"
            if ground_truth == "no" and res_object["correct"] == "yes":
                row[f"r{i + 1}"] = "FN"
            if ground_truth == "yes" and res_object["correct"] == "no":
                row[f"r{i + 1}"] = "FP"
            row[f"exp{i + 1}"] = ""

        # get similarity score when multiple responses generated for a code snippet
        if len(responses) > 1:
            sim_scores = get_cosine_similarity(responses)
            # 0.95 is based on comparing similarity scores on known responses
            row["similar"] = np.all(sim_scores > 0.95)
        rows.append(row)

    report_df = pd.DataFrame.from_dict(rows)
    report_df.to_csv(
        os.path.join(results_path, f"detection_results_{response_dir_name}.csv"),
        sep=",",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate reports by comparing LLM responses to ground truth"
    )

    parser.add_argument(
        "-f",
        "--file",
        type=str,
        required=True,
        help="Require a JSON file with misuses in data directory",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="Results directory name (should be in results directory)",
    )
    parser.add_argument(
        "-s",
        "--prompt-style",
        type=str,
        default="zero-shot",
        choices=["zero-shot", "few-shot"],
        help="Style of the prompt used to generate responses (zero-shot or few-shot)",
    )
    parser.add_argument(
        "-p",
        "--prompt",
        type=str,
        default="base",
        choices=["base", "dtype", "directive", "full"],
    )
    parser.add_argument(
        "-e",
        "--example-type",
        type=str,
        choices=["static", "tailored"],
        help="Type of examples used in the prompt (static or tailored)",
    )

    args = parser.parse_args()

    data_file = os.path.join(os.path.dirname(__file__), "../data", args.file)
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Could not find {args.file}")

    results_path = os.path.join(os.path.dirname(__file__), "../results", args.output)
    if not os.path.exists(results_path):
        raise FileNotFoundError(f"Could not find {args.output}")

    if args.prompt_style == "few-shot" and not args.example_type:
        raise ValueError("Example type is required for few-shot prompt style")

    if args.prompt_style == "few-shot":
        response_dir_name = f"{args.prompt_style}_{args.example_type}_{args.prompt}"
    else:
        response_dir_name = args.prompt

    if not os.path.exists(os.path.join(results_path, "responses", response_dir_name)):
        raise FileNotFoundError(
            f"Could not find {args.prompt_style}_{args.example_type}_{args.prompt} response directory"
        )

    generate_detection_results_report(data_file, results_path, response_dir_name)
