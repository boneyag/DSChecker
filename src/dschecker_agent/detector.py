import argparse
import json
import os
import subprocess

from dschecker.logging_util.logger import setup_logger
from dschecker.models.models import Model
from dschecker.utils.prompt_helper import add_line_numbers_to_code
import dschecker_agent.llm_functions as func
from dschecker_agent.prompt_generator import generate_prompt
import dschecker_agent.tools as t

logger = setup_logger(__name__)


def setup_results_dubdirs(output):
    THIS_PATH = os.path.join(os.path.dirname(__file__))
    os.makedirs(os.path.join(THIS_PATH, "../results", output, "prompts"), exist_ok=True)
    os.makedirs(os.path.join(THIS_PATH, "../results", output, "messages"), exist_ok=True)
    os.makedirs(os.path.join(THIS_PATH, "../results", output, "responses"), exist_ok=True)
    os.makedirs(os.path.join(THIS_PATH, "../results", output, "instrumented"), exist_ok=True)

    # copy the required data files that source code read from
    from_dir = os.path.join(THIS_PATH, "../data/code_snippets")
    to_dir = os.path.join(THIS_PATH, f"../results/{output}/instrumented")
    cp_command = rf"find {from_dir} -maxdepth 1 -type f -name '*.csv' -exec cp {{}} {to_dir} \;"

    try:
        res = subprocess.run(
            cp_command,
            shell=True,
            check=True,  # This will raise a CalledProcessError if the command fails
            capture_output=True,
            text=True
        )
        print("Files copied successfully.")
        if res.stdout:
            print("Stdout:", res.stdout)
        if res.stderr:
            print("Stderr:", res.stderr)
    except subprocess.CalledProcessError as e:
        print("An error occurred while copying files.")
        print("Return code:", e.returncode)
        print("Stdout:", e.stdout)
        print("Stderr:", e.stderr)


def detect_misuses(model, input_data, instance_num, repeats, output):
    setup_results_dubdirs(output)

    if instance_num:
        detect_a_misuse(model, input_data[instance_num], repeats, output)
    else:
        for k in input_data.keys():
            logger.info(k)
            # detect_a_misuse(model, input_data[k], repeats, output)


def detect_a_misuse(model, instance, repeats, output):
    if os.path.exists(
        os.path.join(os.path.dirname(__file__), "../data", instance["code_file_rel_path"])
    ):
        with open(
            os.path.join(os.path.dirname(__file__), "../data", instance["code_file_rel_path"])
        ) as f:
            code_snippet = f.read()
            code_snippet_with_line_nums = "\n".join(
                add_line_numbers_to_code(code_snippet)
            )
    else:
        raise OSError(f"{instance['code_file_rel_path']} does not exist.")

    prompt = generate_prompt(
        lib=instance['lib'],
        code=code_snippet_with_line_nums
    )

    with open(os.path.join(os.path.dirname(__file__), "templates/resources/system.txt")) as f:
        sys_content = f.read()
    messages = [
        {
            "role": "system",
            "content": sys_content
        }
    ]
    messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )
    # logger.info(messages)

    model = Model(model_name=model)

    report = {
        "num": instance["num"],
        "source": instance["source"],
        "lib": instance["lib"],
        "lib_version": instance["lib_version"],
        "code_file_path": instance["code_file_rel_path"],
    }

    if repeats == 1:
        response = get_llm_response(model, messages, instance, output)
        # logger.info(response)

        write_files(
            prompt=messages[1]["content"],
            instance=instance["num"],
            response=response,
            messages=messages,
            output=output,
        )

        report["prompt_file_path"] = (
            f"results/{output}/prompts/{instance['num']}.txt"
        )
        report["messages_file_path"] = (
            f"results/{output}/messages/{instance['num']}.json"
        )
        report["response_file_path"] = (
            f"results/{output}/responses/{instance['num']}.json"
        )

        write_or_update_report(report=report, output=output)
    else:
        for i in range(1, repeats + 1):
            response = get_llm_response(model, messages, instance, output)
            # logger.info(response)

            write_files(
                prompt=messages[1]["content"],
                instance=instance["num"],
                response=response,
                messages=messages,
                output=output,
                repeat_i=i,
            )

            messages = clean_tool_calls_in_messages(messages)

        report["prompt_file_path"] = (
            f"results/{output}/prompts/{instance['num']}.txt"
        )
        report["messages_file_path"] = []
        report["response_file_path"] = []
        for i in range(1, repeats + 1):
            report["messages_file_path"].append(
                f"results/{output}/messages/{instance['num']}_{i}.json"
            )
            report["response_file_path"].append(
                f"results/{output}/responses/{instance['num']}_{i}.json"
            )

        write_or_update_report(report=report, output=output)


def clean_tool_calls_in_messages(messages):
    """Clean content belongs to roles assistant and tool"""
    cleaned_messages = []
    for message in messages:
        if message["role"] in ["system", "user"]:
            cleaned_messages.append(message)
        # Skip messages with role "assistant" that have "tool_calls"
        # Skip messages with role "tool"
    assert cleaned_messages[0]['role'] == "system", "Wrong order of messages"
    assert cleaned_messages[1]['role'] == "user", "Wrong order of messages"
    return cleaned_messages


def get_llm_response(model, messages, instance, output):
    intermediate_response = model.generate(
        messages=messages,
        temperature=0.0,
        tools=t.tools,
        tool_choice="auto"
    )

    intermediate_response_json = json.loads(
        intermediate_response.model_dump_json(indent=4)
    )
    logger.info(f"Finished reason: {intermediate_response_json['choices'][0]['finish_reason']}")

    while intermediate_response_json["choices"][0]["finish_reason"] == 'tool_calls':
        tool_call_messages = {
            "role": "assistant",
            "tool_calls": intermediate_response_json["choices"][0]["message"]["tool_calls"]
        }
        messages.append(tool_call_messages)
        for t_call in tool_call_messages["tool_calls"]:
            tool_call_id = t_call["id"]
            tool_function_name = t_call["function"]["name"]
            tool_args = json.loads(t_call["function"]["arguments"])

            logger.info(f"Tool call: {tool_function_name}")
            logger.info(f"Tool args: {tool_args}")

            if tool_function_name == "get_variable_information":
                func_call_results = func.get_variable_information(
                    tool_args["variable_name"],
                    tool_args["line_number"],
                    instance["code_file_rel_path"],
                    output
                )
            elif tool_function_name == "get_api_documentation":
                func_call_results = func.get_api_documentation(
                    tool_args["api_name"],
                    instance["code_file_rel_path"]
                )
            else:
                func_call_results = "Not an available function. Follow the system prompt to find available functions"
            function_call_result_message = {
                "role": "tool",
                "content": func_call_results,
                "tool_call_id": tool_call_id
            }
            # logger.info(f"Function call result: {func_call_results}")
            messages.append(function_call_result_message)

        # call the model again with the function call responses
        intermediate_response = model.generate(messages, temperature=0.0, tools=t.tools, tool_choice="auto")
        intermediate_response_json = json.loads(
            intermediate_response.model_dump_json(indent=4)
        )
    else:
        logger.info(f"Finish reason: {intermediate_response_json["choices"][0]["finish_reason"]}")
        final_response = intermediate_response_json["choices"][0]["message"]["content"]

    return final_response


def write_files(prompt, instance, response, messages, output, repeat_i=0):
    THIS_PATH = os.path.join(os.path.dirname(__file__))
    PROMPT_PATH = os.path.join(THIS_PATH, "../results", output, "prompts")
    MESSAGE_PATH = os.path.join(THIS_PATH, "../results", output, "messages")
    RESPONSE_PATH = os.path.join(THIS_PATH, "../results", output, "responses")

    with open(os.path.join(PROMPT_PATH, f"{instance}.txt"), "w") as f:
        f.write(prompt)
    if repeat_i == 0:
        with open(
            os.path.join(MESSAGE_PATH, f"{instance}.json"), "w"
        ) as f:
            json.dump(messages, f, indent=4)
        with open(
            os.path.join(RESPONSE_PATH, f"{instance}.json"), "w"
        ) as f:
            json.dump(response, f, indent=4)
    else:
        with open(
            os.path.join(
                MESSAGE_PATH, f"{instance}_{repeat_i}.json"
            ),
            "w",
        ) as f:
            json.dump(messages, f, indent=4)
        with open(
            os.path.join(
                RESPONSE_PATH, f"{instance}_{repeat_i}.json"
            ),
            "w",
        ) as f:
            json.dump(response, f, indent=4)
    logger.info(f"Files written for instance {instance} in {output}")


def write_or_update_report(report, output):
    THIS_PATH = os.path.join(os.path.dirname(__file__))
    if not os.path.exists(
        os.path.join(THIS_PATH, "../results", output, f"report.json")
    ):
        with open(
            os.path.join(THIS_PATH, "../results", output, f"report.json"),
            "w",
        ) as f:
            reports = {}
            reports[report["num"]] = report
            json.dump(reports, f, indent=4)
    else:
        with open(
            os.path.join(THIS_PATH, "../results", output, f"report.json"),
            "r",
        ) as f:
            reports = json.load(f)
        reports[report["num"]] = report
        with open(
            os.path.join(THIS_PATH, "../results", output, f"report.json"),
            "w",
        ) as f:
            json.dump(reports, f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="API misuse detector -- agentic(uses function calling)")

    parser.add_argument(
        '-m',
        '--model',
        type=str,
        default="gpt-4o-2024-05-13",
        choices=[
            "gpt-4o-mini-2024-07-18",
            "gpt-4o-2024-05-13",
            "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        ],
    )
    parser.add_argument(
        '-f',
        '--input-file',
        type=str,
        required=True,
        help="Misuse data file (should be a JSON in data directory)"
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        required=True,
        help="Directory name to create to store prompts and results"
    )
    parser.add_argument(
        '-r',
        '--repeats',
        type=int,
        default=1,
        help="Number of times to prompt LLM"
    )
    parser.add_argument(
        '-i',
        '--instance',
        type=str,
        help="If provided, the detector will only run for that instance. Otherwise, it will loop through the instances in the input file and run for all"
    )

    args = parser.parse_args()

    input_file = os.path.join(os.path.dirname(__file__), "../data/", f"{args.input_file}")
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Could not find {args.input_file}")
    else:
        with open(input_file) as f:
            input_data = json.load(f)

    detect_misuses(args.model, input_data, args.instance, args.repeats, args.output)
