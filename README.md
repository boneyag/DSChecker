## DSChecker

LLM-based Python DS (data science) API misuse detector and fixer

### Steps to run the project
1. Clone this repo `git clone <repo-url>`.
2. We use [uv](https://docs.astral.sh/uv/getting-started/installation/) to manage dependencies and run the project. To start, run `uv pip install -r pyproject.toml` to install dependencies in the virtual environment (you will see a directory `.venv` after running this). You can also create a virtual environment (`python3 -m venv <your-venv-name>`) and then install the dependencies using `pip install -r requirements.txt` from the requirement file given.
3. 

### Project content

#### DSChecker

This is the main part of the project. `dschecker` contains the main executable scripts which we describe in the following subtopic.

##### Main executables
Note that we are using `uv` package manager. To run a script, move to the project root, and then run `PYTHONPATH=src uv run src/dschecker/detector.py`.
1. `detector.py` - This script prompt LLM to detect and fix API misuses in code snippets. It takes a several command line arguments.
    - `--model` - Name of different LLMs accepted by the API (e.g., `gpt4o-mini` to access the latest mini model in OpenAI's API). The argument has all the supported models listed as choices.
    - `--style` - Currently we support zero-shot and few-shot style prompts. Note that, few-shot prompt only provide two examples. The default is zero-shot.
    - `--prompt` - Prompt type can be either `base`, `dtype`, `directive`, or `full`. `base` provide the basic information such as the code snippet and the library name. `dtype` include information of the variables processed by an API in the code. `directive` provide documented usage instructions of an API, if available. `full` combines the `dtype` and `directive`. If the `--style` is few-shot, it will have different information according to the `--prompt` option selected. For example, if `--style` is few-shot and `--prompt` is dtype, then the examples in the prompt will contain information about the variables as well as the code in question.
    - `--example-type` - If the `--style` is few-shot, this argument will decide if the prompt will contain static examples (i.e., same example code will be used in all prompts) or tailored examples to the code in question (e.g., we provide the most similar example code that uses the same library as the code in question).
    - `--file` - Misuse file (should be a JSON). We will look for a JSON file in data directory. This cannot be any JSON as we expect a specific schema. So, we recommend the `API_misuses.json` file. If you need to use your own, create a new one following the same schema.
    - `--repeat` - Number of times the prompt should be repeated with LLM. The default is 1. This option is available if you need to run the same misuse multiple times as observe if the LLM provide variable responses due to its non-deterministic nature.
    - `--instance` - Instance number as stated in the JSON file input for `--file`. If this argument is ignored, the script will run for all instances in the JSON file. If provided, it will only run for that specific instance. This is useful to see if the code is running correctly and reports are generated correctly.
    - `--output` - The directory name to store the results. This will be created in the `results` directory. Each `--output` directory contains two subdirectories: prompts and responses. In addition to that, there will be reports for each prompt style.

The detector make use of different modules: `model`, `template`. `model` contains a script that generate an LLM model. `template` contains a script that generate various prompt templates and prompts.   
2. `prompt_generator.py` - Generate different prompts according to instructions passed from the detector.py script.
3. `results_report_generator.py` - This script takes 3 command line arguments.
    - `--file` - JSON file containing misuses (it should be in the data directory)
    - `--output` - Directory name of the results stored (usually created by the `detector.py` script)
    - `--prompt` - prompt type (`detectory.py` creates a sub-directory in the `--output`/`responses` directory which stores the LLMs resonses)
    The script compares the LLM's response with the ground truth in the `--file` and then generates a report if the initial detection is either TP, FP, TN, or FN.
    This script uses response similarity calculator to compare pairs of responses. If at least one pair has a similarity score less than 0.95, it records false. This indicates to manual evaluators to check for all responses instead of one random response.

#### DSChecker-agent
This is the function calling part of the project. `dschecker_agent` contains the main executable scripts which we describe in the following subtopic.

##### Main executables
Note that we are using `uv` package manager. To run a script, move to the project root, and then run `PYTHONPATH=src uv run src/dschecker_agent/detector.py`.
1. `detector.py` - This script prompt LLM to detect and fix API misuses in code snippets. It takes a several command line arguments.
    - `--model` - Name of different LLMs accepted by the API (e.g., `gpt4o-mini` to access the latest mini model in OpenAI's API). The argument has all the supported models listed as choices.
    - `--file` - Misuse file (should be a JSON). We will look for a JSON file in data directory. This cannot be any JSON as we expect a specific schema. So, we recommend the `API_misuses.json` file. If you need to use your own, create a new one following the same schema.
    - `--repeat` - Number of times the prompt should be repeated with LLM. The default is 1. This option is available if you need to run the same misuse multiple times as observe if the LLM provide variable responses due to its non-deterministic nature.
    - `--instance` - Instance number as stated in the JSON file input for `--file`. If this argument is ignored, the script will run for all instances in the JSON file. If provided, it will only run for that specific instance. This is useful to see if the code is running correctly and reports are generated correctly.
    - `--output` - The directory name to store the results. This will be created in the `results` directory. Each `--output` directory contains three subdirectories: prompts, responses, and messages. Messages directory is the new introduction in agent. This directory stores function calls and their responses for analysis. In addition to that, there will be reports for each prompt style.
*Note: We do not support prompt variations yet. Therefore, this script does not ask for prompt and related args (e.g., zero-shot vs. few-shot, example type for few-shot).*
2. `prompt_generator.py` - Same as the script in `dschecker` module.
3. `patch_runner.py` and `results_report_generator.py` - Similar to the scripts in `dschecker` module. Since we don't use prompt styles, prompt variations, etc., I have these two redundant script with less command line args. *Probably refactor in future.*
4. `tools.py` - Contains function description (JSON object) to inform LLM which functions are available.
5. `llm_function.py` - The actual functions that llm request to invoke.
6. `llm_function_utils.py` - Support functions for `llm_functions.py`. For example, there are classes that analyze AST to get fully qualified name, instrument the code to get variable information etc. 

##### Supporting modules
* `indexer` - This module contains the scripts to generate a local index of API docs, search docs, etc. The html files that we index are in the `html` directory. You will not see the `html` directory as we do not push to remote. Therefore, if you need to generate an index, put the files in here. Note that, it is recommended to create subdirectories for each library and put the htmls directly in there instead of creating additional subdirectories. We create the index using `whoosh`. The index is stored in `docindex`. We push this to remote. So, you can simply do the searching without creating the index on your own.

#### Data 
`data` directory contains the `API_misuses.json` file which contains the metadata of each instance (we use the term instance, because the dataset contains both misuses and their corresponding fixed code). There are two subdirectories: `code_snippets` and `patches`. The former contain the source codes and the latter contains the patches that fix misuses. To easily identify and relate source code with its metadata in the JSON file, source files are named like `<#>_<lib>_<api>.py`. For example, `1_scikitlearn_onehotencoder.py` contains a misuse from the scikit-learn library which involves `OneHotEncoder`. The number `1` matches to the key in the JSON. Note that corresponding fixes of each source code has the number followed by the letter 'c' (e.g., `1c_scikitlearn_onehotencoder.py`). Patches also follow a similar naming pattern. For the above misuse, the corresponding patch named as `1_scikitlearn_onehotencoder_patch.txt`.

##### Clients
Currently, we support two clients: OpenAI and TogetherAI.

We have the abstract class Client (`client.py`) which then inherit by OpenAI client (`openai_client.py`) and TogetherAI client (`togetherai_client.py`). This was design allows including more clients in the future. However, the Client class expect the model to work with OpenAI's API. Therefore, adding Google's models is not compatible right now.

##### Models

Currently, we support three models: `gpt4o` and `gpt4o-mini` from OpenAI and `llama-3.1-405b-instruct-turbo` from meta (this model is served by TogetherAI).

##### Templates

The `template` directory contains a set of text files (in the subdirectory `resources`) which allow us to generate prompt templates. Each text file contains static text and placeholders (starts with '$' sign). The `template.py` contains classes which uses the text files to generate prompts programmatically. Each class has `get_text(self, **kwargs)` method which safely substitute values with placeholders in the template and then returns the prompt.

##### Logging

We have `logging_util` directory which provides the means to set up a logger. 

##### Utilities

The `utils` directory contains support functions.
1. `prompt_helper` has a function that add line numbers to source code. This is important when generating prompts so that the LLM can refer to those line number when explaining problems, etc.
2. `response_similarity_calculator.py` has function that calculate cosine similarity between pairs of vector embeddings (embedding created using OpenAI's `text-embedding-3-small`). It returns a list of similarity scores. 

#### Vector DB

We use Chroma DB client to store vectorized source code snippets. The purpose is to find similar code snippets for a given code snippet which will be used to generate taylored few-shot prompts. The `vector_db` directory contains the source code that populate, search the Chroma DB and update the `API_misuses.json` in `data` directory with similarity IDs.

- `storage` directory contains the persistant Chroma database.
- `models` directory contains language model (in our case codebert) for encoding documents. If you use an API such as OpenAI for encoding, you don't need this. Create this directory and paste your model, if you want access to local model.
- `database.py` contains the logic to populate the database and search.
- `add_documents.py` contains the logic to insert documents to the database. We specifically pick metadata from the `API_misuses.json` file (e.g., library name, ID, etc.) to create metadata for each document (in our case, documents are source code) which will be useful when filtering similar codes.
- `search_documents.py` contains the logic to search similar codes (misuses and correct versions).  

### Running tests
The project uses `pytest`.

To run the test, first move to the project root (you should see the `src` and `tests` directories in there) and run ``PYTHONPATH=src uv run pytest`.

Current tests
* Prompt tests
    - Zero-shot: Base, Dtype, Directive, and Full (only happy path and a few edge cases)
