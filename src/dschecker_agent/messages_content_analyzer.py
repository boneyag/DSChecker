'''
This scripts analyzes the messages in results directory. This is purely for analysis purposes. We wanted to know the functions LLM called for each instance and the arguments it passed to those function calls. We'll also compare the args with API_misuses.json file to see if it called for APIs and variables recorded in the dataset file as well.
'''

import argparse
import json
import os
import pandas as pd

CURR_DIR = os.path.dirname(__file__)


def messages_analyzer(res_dir, msg_dir, misuse_data_file, repeats):
    report = {}

    msg_file_list = os.listdir(msg_dir)

    with open(misuse_data_file) as mdf:
        misuse_data = json.load(mdf)

    for k, v in misuse_data.items():
        grouped_row = {}
        for i in range(1, repeats + 1):
            if f"{k}_{i}.json" in msg_file_list:
                with open(os.path.join(msg_dir, f"{k}_{i}.json")) as msg_f:
                    msg_content = json.load(msg_f)
                total_calls = 0
                doc_calls = 0
                var_calls = 0
                api_name = ""
                var_name = ""
                for msg in msg_content:
                    if "tool_calls" in msg:
                        total_calls += len(msg["tool_calls"])
                        for tc in msg["tool_calls"]:
                            if tc["function"]["name"] == "get_api_documentation":
                                doc_calls += 1
                                if v["directive"]["api"] != "" and v["directive"]["api"] in tc["function"]["arguments"]:
                                    api_name = v["directive"]["api"]
                            if tc["function"]["name"] == "get_variable_information":
                                var_calls += 1
                                if v["api_misuse"]["data"]["variable_name"] in tc["function"]["arguments"]:
                                    var_name = v["api_misuse"]["data"]["variable_name"]

                grouped_row[(i, "total")] = total_calls
                grouped_row[(i, "doc_calls")] = doc_calls
                grouped_row[(i, "var_calls")] = var_calls
                grouped_row[(i, "api_name")] = api_name
                grouped_row[(i, "var_name")] = var_name
        report[k] = grouped_row

    df = pd.DataFrame.from_dict(report, orient='index')
    df.to_csv(os.path.join(res_dir, "msg_report.csv"))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-d',
        '--results-directory',
        type=str,
        required=True
    )
    parser.add_argument(
        '-f',
        '--misuse-data-file',
        type=str,
        required=True
    )
    parser.add_argument(
        '-r',
        '--repeats',
        type=int,
        required=True,
    )

    args = parser.parse_args()

    # first check if the results directory exists
    res_dir = os.path.join(CURR_DIR, "../results", args.results_directory)
    if not os.path.exists(res_dir):
        raise FileNotFoundError(f"{args.results_directory} does not exist.")

    # then check if the messages exists in there (only function calling experiments has this dir)
    msg_dir = os.path.join(res_dir, "messages")
    if not os.path.exists(msg_dir):
        raise FileNotFoundError(f"{args.results_directory} does not contain a messages directory.")

    data_file = os.path.join(CURR_DIR, "../data/", f"{args.misuse_data_file}")
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"{args.misuse_data_file} does not exist.")
    
    messages_analyzer(res_dir, msg_dir, data_file, args.repeats)
