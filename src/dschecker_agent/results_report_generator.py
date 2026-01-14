import argparse
import ast
import json
import os

import numpy as np
import pandas as pd

from dschecker.logging_util.logger import setup_logger
from dschecker.utils.response_similarity_calculator import get_cosine_similarity

logger = setup_logger(__name__)


def generate_detection_results_report(data_file, results_path):
    with open(data_file) as f:
        data = json.load(f)

    with open(os.path.join(results_path, "report.json")) as f:
        results = json.load(f)

    rows = []
    for k, v in results.items():
        ground_truth = data[k]["correct"]
        row = {}
        row["num"] = k
        responses = []
        for i, res_report_path in enumerate(v["response_file_path"]):
            with open(os.path.join(os.path.dirname(__file__), "../", res_report_path), "r") as f:
                json_string = json.load(f)
            try:
                res_object = ast.literal_eval(
                    json_string
                )  # workaround -- json.load return str instead of dict
            except SyntaxError:
                logger.error(f"Error parsing JSON output for {k}--{i+1}")
                continue

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
        os.path.join(results_path, "detection_results.csv"),
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

    args = parser.parse_args()

    data_file = os.path.join(os.path.dirname(__file__), "../data", args.file)
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Could not find {args.file}")

    results_path = os.path.join(os.path.dirname(__file__), "../results", args.output)
    if not os.path.exists(results_path):
        raise FileNotFoundError(f"Could not find {args.output}")

    generate_detection_results_report(data_file, results_path)
