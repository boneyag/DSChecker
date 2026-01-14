import pytest
from dschecker.templates.template import (
    Base,
    Directive,
    Dtype,
    Full,
    get_dynamic_fewshot_static_class,
    get_dynamic_fewshot_tailored_class
)


MOCKED_FILE_CONTENTS = {
    "task.txt": "The code provided uses the library $lib.\nCheck this piece of code and decide if it correctly uses library $lib.",
    "response.txt": "Respond exactly in the following JSON format. If the code is correct, leave the remaining fields empty after setting field \"correct\" to yes:\n{\n  \"correct\": \"yes/no\",\n  \"explanation\": \"explanation of why the code is incorrect\",\n  \"patch\": \"Provide normal diff format output that can be used to patch the buggy code (e.g., 19c19,20\\n<foo()\\n---\\n>foo(bass='bazz')\\n>bar()). Consider indentation when creating the patch.\"\n}\n\nHere is the code to inspect.\nThe numbers on the left-hand side of the code represent line numbers (as shown in an IDE or text editor) and are not part of the actual code.\n\n$code\n\nYour response:",
    "directive_api.txt": "$lib documentation states this guideline \"$directive\" for $api API, which could be useful to decide if the code correctly uses the library.",
    "directive_param.txt": "$lib documentation states this guideline \"$directive\" for $parameter parameter of $api API, which could be useful to decide if the code correctly uses the library.",
    "directive_other.txt": "$lib documentation states this guideline \"$directive\", which could be useful to decide if the code correctly uses the library.",
    "data_type_sample.txt": "Here is information about the variable $variable at line $linenum used in this code snippet.\n\ntype: $type\n\nadditional information: \n$additional\n\nsample: \n$sample",
    "data_type.txt": "Here is information about the variable $variable at line $linenum used in this code snippet.\n\ntype: $type\n\nadditional information: \n$additional"
}

@pytest.fixture(autouse=True)
def mock_read_templates(mocker):
    def mock_internal_read_file(file_key):
        file_name_map = {
            "task": "task.txt",
            "response": "response.txt",
            "api": "directive_api.txt",
            "param": "directive_param.txt",
            "other": "directive_other.txt",
            "data": "data_type_sample.txt",
            "type": "data_type.txt"
        }
        mock_file_name = file_name_map.get(file_key)
        if mock_file_name in MOCKED_FILE_CONTENTS:
            return MOCKED_FILE_CONTENTS[mock_file_name]
        raise ValueError(f"No file content found for file key: {file_key}")

    mocker.patch("dschecker.templates.template._read_file", side_effect=mock_internal_read_file)
    yield


def test_base_prompt():
    template = Base(lib="pandas", code="1    import pandas as pd\n2    df = pd.DataFrame()")
    prompt = template.get_text()
    assert prompt == (
        "The code provided uses the library pandas.\n"
        "Check this piece of code and decide if it correctly uses library pandas.\n\n"
        "Respond exactly in the following JSON format. If the code is correct, leave the remaining fields empty after setting field \"correct\" to yes:\n{\n  \"correct\": \"yes/no\",\n  \"explanation\": \"explanation of why the code is incorrect\",\n  \"patch\": \"Provide normal diff format output that can be used to patch the buggy code (e.g., 19c19,20\\n<foo()\\n---\\n>foo(bass='bazz')\\n>bar()). Consider indentation when creating the patch.\"\n}\n\nHere is the code to inspect.\nThe numbers on the left-hand side of the code represent line numbers (as shown in an IDE or text editor) and are not part of the actual code.\n\n1    import pandas as pd\n2    df = pd.DataFrame()\n\nYour response:"
    )


def test_directive_prompt_api():
    template = Directive(directive_type="api", lib="pandas", code="1    import pandas as pd\n2    df = pd.DataFrame()", directive="Do not use chain indexing...", api="replace", parameter="")
    prompt = template.get_text()
    assert prompt == (
        "The code provided uses the library pandas.\n"
        "Check this piece of code and decide if it correctly uses library pandas.\n\n"
        "pandas documentation states this guideline \"Do not use chain indexing...\" for replace API, which could be useful to decide if the code correctly uses the library.\n\n"
        "Respond exactly in the following JSON format. If the code is correct, leave the remaining fields empty after setting field \"correct\" to yes:\n{\n  \"correct\": \"yes/no\",\n  \"explanation\": \"explanation of why the code is incorrect\",\n  \"patch\": \"Provide normal diff format output that can be used to patch the buggy code (e.g., 19c19,20\\n<foo()\\n---\\n>foo(bass='bazz')\\n>bar()). Consider indentation when creating the patch.\"\n}\n\nHere is the code to inspect.\nThe numbers on the left-hand side of the code represent line numbers (as shown in an IDE or text editor) and are not part of the actual code.\n\n1    import pandas as pd\n2    df = pd.DataFrame()\n\nYour response:"
    )


def test_directive_prompt_param():
    template = Directive(directive_type="param", lib="pandas", code="1    import pandas as pd\n2    df = pd.DataFrame()", directive="Do not use chain indexing...", api="replace", parameter="inplace")
    prompt = template.get_text()
    assert prompt == (
        "The code provided uses the library pandas.\n"
        "Check this piece of code and decide if it correctly uses library pandas.\n\n"
        "pandas documentation states this guideline \"Do not use chain indexing...\" for inplace parameter of replace API, which could be useful to decide if the code correctly uses the library.\n\n"
        "Respond exactly in the following JSON format. If the code is correct, leave the remaining fields empty after setting field \"correct\" to yes:\n{\n  \"correct\": \"yes/no\",\n  \"explanation\": \"explanation of why the code is incorrect\",\n  \"patch\": \"Provide normal diff format output that can be used to patch the buggy code (e.g., 19c19,20\\n<foo()\\n---\\n>foo(bass='bazz')\\n>bar()). Consider indentation when creating the patch.\"\n}\n\nHere is the code to inspect.\nThe numbers on the left-hand side of the code represent line numbers (as shown in an IDE or text editor) and are not part of the actual code.\n\n1    import pandas as pd\n2    df = pd.DataFrame()\n\nYour response:"
    )


def test_directive_prompt_other():
    template = Directive(directive_type="other", lib="pandas", code="1    import pandas as pd\n2    df = pd.DataFrame()", directive="Do not use chain indexing...", api="", parameter="")
    prompt = template.get_text()
    assert prompt == (
        "The code provided uses the library pandas.\n"
        "Check this piece of code and decide if it correctly uses library pandas.\n\n"
        "pandas documentation states this guideline \"Do not use chain indexing...\", which could be useful to decide if the code correctly uses the library.\n\n"
        "Respond exactly in the following JSON format. If the code is correct, leave the remaining fields empty after setting field \"correct\" to yes:\n{\n  \"correct\": \"yes/no\",\n  \"explanation\": \"explanation of why the code is incorrect\",\n  \"patch\": \"Provide normal diff format output that can be used to patch the buggy code (e.g., 19c19,20\\n<foo()\\n---\\n>foo(bass='bazz')\\n>bar()). Consider indentation when creating the patch.\"\n}\n\nHere is the code to inspect.\nThe numbers on the left-hand side of the code represent line numbers (as shown in an IDE or text editor) and are not part of the actual code.\n\n1    import pandas as pd\n2    df = pd.DataFrame()\n\nYour response:"
    )


def test_directive_prompt_with_empty_directive():
    template = Directive(
        directive_type="",
        lib="pandas",
        code="1    import pandas as pd\n2    df = pd.DataFrame()",
        directive="",
        api="",
        parameter=""
    )
    prompt = template.get_text()
    assert prompt == (
        "The code provided uses the library pandas.\n"
        "Check this piece of code and decide if it correctly uses library pandas.\n\n"
        "Respond exactly in the following JSON format. If the code is correct, leave the remaining fields empty after setting field \"correct\" to yes:\n{\n  \"correct\": \"yes/no\",\n  \"explanation\": \"explanation of why the code is incorrect\",\n  \"patch\": \"Provide normal diff format output that can be used to patch the buggy code (e.g., 19c19,20\\n<foo()\\n---\\n>foo(bass='bazz')\\n>bar()). Consider indentation when creating the patch.\"\n}\n\nHere is the code to inspect.\nThe numbers on the left-hand side of the code represent line numbers (as shown in an IDE or text editor) and are not part of the actual code.\n\n1    import pandas as pd\n2    df = pd.DataFrame()\n\nYour response:"
    )


def test_dtype_prompt_with_no_sample():
    template = Dtype(add_sample=False, lib="pandas", code="1    import pandas as pd\n2    df = pd.DataFrame()", variable="df", linenum=2, type="pandas.core.frame.DataFrame", additional="RangeIndex: 4 entries, 0 to 3\nData columns (total 4 columns):\n #   Column         Non-Null Count  Dtype \n---  ------         --------------  ----- \n 0   city           4 non-null      object\n 1   country        4 non-null      object\n 2   expert_rating  4 non-null      int64 \n 3   user_rating    4 non-null      int64 \ndtypes: int64(2), object(2)", sample="      city country  expert_rating  user_rating\n0   London      UK              5            4\n1   London     0.2              3            5\n2    Paris      FR              4            4\n3  NewYork      US              5            3")
    prompt = template.get_text()
    assert prompt == (
        "The code provided uses the library pandas.\n"
        "Check this piece of code and decide if it correctly uses library pandas.\n\n"
        "Here is information about the variable df at line 2 used in this code snippet.\n"
        "\ntype: pandas.core.frame.DataFrame\n\n"
        "additional information: \nRangeIndex: 4 entries, 0 to 3\nData columns (total 4 columns):\n #   Column         Non-Null Count  Dtype \n---  ------         --------------  ----- \n 0   city           4 non-null      object\n 1   country        4 non-null      object\n 2   expert_rating  4 non-null      int64 \n 3   user_rating    4 non-null      int64 \ndtypes: int64(2), object(2)\n\n"
        "Respond exactly in the following JSON format. If the code is correct, leave the remaining fields empty after setting field \"correct\" to yes:\n{\n  \"correct\": \"yes/no\",\n  \"explanation\": \"explanation of why the code is incorrect\",\n  \"patch\": \"Provide normal diff format output that can be used to patch the buggy code (e.g., 19c19,20\\n<foo()\\n---\\n>foo(bass='bazz')\\n>bar()). Consider indentation when creating the patch.\"\n}\n\nHere is the code to inspect.\nThe numbers on the left-hand side of the code represent line numbers (as shown in an IDE or text editor) and are not part of the actual code.\n\n1    import pandas as pd\n2    df = pd.DataFrame()\n\nYour response:"
    )


def test_dtype_prompt_with_sample():
    template = Dtype(add_sample=True, lib="pandas", code="1    import pandas as pd\n2    df = pd.DataFrame()", variable="df", linenum=2, type="pandas.core.frame.DataFrame", additional="RangeIndex: 4 entries, 0 to 3\nData columns (total 4 columns):\n #   Column         Non-Null Count  Dtype \n---  ------         --------------  ----- \n 0   city           4 non-null      object\n 1   country        4 non-null      object\n 2   expert_rating  4 non-null      int64 \n 3   user_rating    4 non-null      int64 \ndtypes: int64(2), object(2)", sample="      city country  expert_rating  user_rating\n0   London      UK              5            4\n1   London     0.2              3            5\n2    Paris      FR              4            4\n3  NewYork      US              5            3")
    prompt = template.get_text()
    assert prompt == (
        "The code provided uses the library pandas.\n"
        "Check this piece of code and decide if it correctly uses library pandas.\n\n"
        "Here is information about the variable df at line 2 used in this code snippet.\n"
        "\ntype: pandas.core.frame.DataFrame\n\n"
        "additional information: \nRangeIndex: 4 entries, 0 to 3\nData columns (total 4 columns):\n #   Column         Non-Null Count  Dtype \n---  ------         --------------  ----- \n 0   city           4 non-null      object\n 1   country        4 non-null      object\n 2   expert_rating  4 non-null      int64 \n 3   user_rating    4 non-null      int64 \ndtypes: int64(2), object(2)\n\n"
        "sample: \n      city country  expert_rating  user_rating\n0   London      UK              5            4\n1   London     0.2              3            5\n2    Paris      FR              4            4\n3  NewYork      US              5            3\n\n"
        "Respond exactly in the following JSON format. If the code is correct, leave the remaining fields empty after setting field \"correct\" to yes:\n{\n  \"correct\": \"yes/no\",\n  \"explanation\": \"explanation of why the code is incorrect\",\n  \"patch\": \"Provide normal diff format output that can be used to patch the buggy code (e.g., 19c19,20\\n<foo()\\n---\\n>foo(bass='bazz')\\n>bar()). Consider indentation when creating the patch.\"\n}\n\nHere is the code to inspect.\nThe numbers on the left-hand side of the code represent line numbers (as shown in an IDE or text editor) and are not part of the actual code.\n\n1    import pandas as pd\n2    df = pd.DataFrame()\n\nYour response:"
    )


def test_dtype_prompt_with_extra_args():
    template = Dtype(add_sample=True,
                     lib="pandas",
                     code="1    import pandas as pd\n2    df = pd.DataFrame()", variable="df",
                     linenum=2,
                     type="pandas.core.frame.DataFrame",
                     additional="RangeIndex: 4 entries, 0 to 3\nData columns (total 4 columns):\n #   Column         Non-Null Count  Dtype \n---  ------         --------------  ----- \n 0   city           4 non-null      object\n 1   country        4 non-null      object\n 2   expert_rating  4 non-null      int64 \n 3   user_rating    4 non-null      int64 \ndtypes: int64(2), object(2)",
                     sample="      city country  expert_rating  user_rating\n0   London      UK              5            4\n1   London     0.2              3            5\n2    Paris      FR              4            4\n3  NewYork      US              5            3",
                     directive="Do not use chain indexing...",
                    api="replace",
                    parameter="inplace")
    prompt = template.get_text()
    assert prompt == (
        "The code provided uses the library pandas.\n"
        "Check this piece of code and decide if it correctly uses library pandas.\n\n"
        "Here is information about the variable df at line 2 used in this code snippet.\n"
        "\ntype: pandas.core.frame.DataFrame\n\n"
        "additional information: \nRangeIndex: 4 entries, 0 to 3\nData columns (total 4 columns):\n #   Column         Non-Null Count  Dtype \n---  ------         --------------  ----- \n 0   city           4 non-null      object\n 1   country        4 non-null      object\n 2   expert_rating  4 non-null      int64 \n 3   user_rating    4 non-null      int64 \ndtypes: int64(2), object(2)\n\n"
        "sample: \n      city country  expert_rating  user_rating\n0   London      UK              5            4\n1   London     0.2              3            5\n2    Paris      FR              4            4\n3  NewYork      US              5            3\n\n"
        "Respond exactly in the following JSON format. If the code is correct, leave the remaining fields empty after setting field \"correct\" to yes:\n{\n  \"correct\": \"yes/no\",\n  \"explanation\": \"explanation of why the code is incorrect\",\n  \"patch\": \"Provide normal diff format output that can be used to patch the buggy code (e.g., 19c19,20\\n<foo()\\n---\\n>foo(bass='bazz')\\n>bar()). Consider indentation when creating the patch.\"\n}\n\nHere is the code to inspect.\nThe numbers on the left-hand side of the code represent line numbers (as shown in an IDE or text editor) and are not part of the actual code.\n\n1    import pandas as pd\n2    df = pd.DataFrame()\n\nYour response:"
    )


def test_full_prompt_with_api_directive_with_no_sample():
    template = Full(directive_type="api", add_sample=False,
                    lib="pandas",
                    code="1    import pandas as pd\n2    df = pd.DataFrame()",
                    directive="Do not use chain indexing...",
                    api="replace",
                    parameter="inplace",
                    variable="df",
                    linenum=2,
                    type="pandas.core.frame.DataFrame",
                    additional="RangeIndex: 4 entries, 0 to 3\nData columns (total 4 columns):\n #   Column         Non-Null Count  Dtype \n---  ------         --------------  ----- \n 0   city           4 non-null      object\n 1   country        4 non-null      object\n 2   expert_rating  4 non-null      int64 \n 3   user_rating    4 non-null      int64 \ndtypes: int64(2), object(2)",
                    sample="      city country  expert_rating  user_rating\n0   London      UK              5            4\n1   London     0.2              3            5\n2    Paris      FR              4            4\n3  NewYork      US              5            3"
                    )
    prompt = template.get_text()
    assert prompt == (
        "The code provided uses the library pandas.\n"
        "Check this piece of code and decide if it correctly uses library pandas.\n\n"
        "pandas documentation states this guideline \"Do not use chain indexing...\" for replace API, which could be useful to decide if the code correctly uses the library.\n\n"
        "Here is information about the variable df at line 2 used in this code snippet.\n"
        "\ntype: pandas.core.frame.DataFrame\n\n"
        "additional information: \nRangeIndex: 4 entries, 0 to 3\nData columns (total 4 columns):\n #   Column         Non-Null Count  Dtype \n---  ------         --------------  ----- \n 0   city           4 non-null      object\n 1   country        4 non-null      object\n 2   expert_rating  4 non-null      int64 \n 3   user_rating    4 non-null      int64 \ndtypes: int64(2), object(2)\n\n"
        "Respond exactly in the following JSON format. If the code is correct, leave the remaining fields empty after setting field \"correct\" to yes:\n{\n  \"correct\": \"yes/no\",\n  \"explanation\": \"explanation of why the code is incorrect\",\n  \"patch\": \"Provide normal diff format output that can be used to patch the buggy code (e.g., 19c19,20\\n<foo()\\n---\\n>foo(bass='bazz')\\n>bar()). Consider indentation when creating the patch.\"\n}\n\nHere is the code to inspect.\nThe numbers on the left-hand side of the code represent line numbers (as shown in an IDE or text editor) and are not part of the actual code.\n\n1    import pandas as pd\n2    df = pd.DataFrame()\n\nYour response:"
    )


def test_full_prompt_with_param_directive_with_sample():
    template = Full(directive_type="param", add_sample=True,
                    lib="pandas",
                    code="1    import pandas as pd\n2    df = pd.DataFrame()",
                    directive="Do not use chain indexing...",
                    api="replace",
                    parameter="inplace",
                    variable="df",
                    linenum=2,
                    type="pandas.core.frame.DataFrame",
                    additional="RangeIndex: 4 entries, 0 to 3\nData columns (total 4 columns):\n #   Column         Non-Null Count  Dtype \n---  ------         --------------  ----- \n 0   city           4 non-null      object\n 1   country        4 non-null      object\n 2   expert_rating  4 non-null      int64 \n 3   user_rating    4 non-null      int64 \ndtypes: int64(2), object(2)",
                    sample="      city country  expert_rating  user_rating\n0   London      UK              5            4\n1   London     0.2              3            5\n2    Paris      FR              4            4\n3  NewYork      US              5            3"
                    )
    prompt = template.get_text()
    assert prompt == (
        "The code provided uses the library pandas.\n"
        "Check this piece of code and decide if it correctly uses library pandas.\n\n"
        "pandas documentation states this guideline \"Do not use chain indexing...\" for inplace parameter of replace API, which could be useful to decide if the code correctly uses the library.\n\n"
        "Here is information about the variable df at line 2 used in this code snippet.\n"
        "\ntype: pandas.core.frame.DataFrame\n\n"
        "additional information: \nRangeIndex: 4 entries, 0 to 3\nData columns (total 4 columns):\n #   Column         Non-Null Count  Dtype \n---  ------         --------------  ----- \n 0   city           4 non-null      object\n 1   country        4 non-null      object\n 2   expert_rating  4 non-null      int64 \n 3   user_rating    4 non-null      int64 \ndtypes: int64(2), object(2)\n\n"
        "sample: \n      city country  expert_rating  user_rating\n0   London      UK              5            4\n1   London     0.2              3            5\n2    Paris      FR              4            4\n3  NewYork      US              5            3\n\n"
        "Respond exactly in the following JSON format. If the code is correct, leave the remaining fields empty after setting field \"correct\" to yes:\n{\n  \"correct\": \"yes/no\",\n  \"explanation\": \"explanation of why the code is incorrect\",\n  \"patch\": \"Provide normal diff format output that can be used to patch the buggy code (e.g., 19c19,20\\n<foo()\\n---\\n>foo(bass='bazz')\\n>bar()). Consider indentation when creating the patch.\"\n}\n\nHere is the code to inspect.\nThe numbers on the left-hand side of the code represent line numbers (as shown in an IDE or text editor) and are not part of the actual code.\n\n1    import pandas as pd\n2    df = pd.DataFrame()\n\nYour response:"
    )


# def test_few_shot_base_with_static_examples():
#     FewshotStaticBase = get_dynamic_fewshot_static_class(Base)
#     fewshot_base_template = FewshotStaticBase() 
