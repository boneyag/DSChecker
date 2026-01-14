import json
import os

from dschecker.logging_util.logger import setup_logger
from dschecker_agent.indexer.search_documents import search_documents_in_index
from dschecker_agent.llm_function_utils import get_fully_qualified_name
from dschecker_agent.llm_function_utils import instrument_code
from dschecker_agent.llm_function_utils import run_code

logger = setup_logger(__name__)

KNOWN_MEMBERS = [
    "fit",
    "transform",
    "fit_transform",
    "predict",
    "predict_proba",
    "score"
]


def get_variable_information(variable_name, line_number, code_file_path, output):
    var_info = {
        "variable_name": variable_name,
        "line_number": line_number,
        "data_type": "",
        "sample": "",
        "additional_info": "",
    }

    with open(os.path.join(os.path.dirname(__file__), "../data", code_file_path)) as f:
        code = f.read()

    file_name = code_file_path.split("/")[-1][:-3]  # remove the path before name and the extension
    instrument_code(variable_name, line_number, code, file_name, output)
    output = run_code(file_name, output)

    if output:
        # remove extra newlines
        output = [line.strip() for line in output]
        # extract only the intrumented output
        start_ind = output.index("----***----")
        end_ind = output.index("----***----", start_ind+1)
        output = output[start_ind+1:end_ind]

        if output and "Unsuported type for instrumentation" in output:
            var_info["data_type"] = output[0].strip()
            var_info["additional_info"] = "Unsupported type"
            var_info["sample"] = "NA"
        else:
            # extract the object type
            var_info["data_type"] = output[0].strip()
            # extract the info
            var_info["additional_info"] = "\n".join(output[1:output.index("***")])
            # extract the sample
            var_info["sample"] = "\n".join(output[output.index("***")+1:])

        # logger.info(f"Data: {var_info}")
        return json.dumps(var_info)
    else:
        return json.dumps({"error": "Error running the instrumented code"})


def get_api_documentation(api_name, code_file_path):
    with open(os.path.join(os.path.dirname(__file__), "../data", code_file_path)) as f:
        code = f.read()

    fqn = get_fully_qualified_name(api_name, code)
    logger.info(f"Returned fqn: {fqn}")
    if fqn:
        name_parts = fqn.split(".")
        simple_name = name_parts[-1]
        if simple_name not in KNOWN_MEMBERS:
            search_res = search_documents_in_index(simple_name)
        else:
            class_name = name_parts[-2]
            search_res = search_documents_in_index(class_name)
        return json.dumps(search_res)
    else:
        return json.dumps(["No results found"])


if __name__ == '__main__':
    path = "code_snippets/50_seaborn_lineplot.py"
    get_variable_information("Y_pred", 20, path, "test")
