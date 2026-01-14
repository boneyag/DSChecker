tools = [
    {
        "type": "function",
        "function": {
            "name": "get_variable_information",
            "description": "Get the type of a variable and a sample of the data of that variable",
            "parameters": {
                "type": "object",
                "properties": {
                    "variable_name": {
                        "type": "string",
                        "description": "The variable name to analyze. This should be the exact name as in the source code."
                    },
                    "line_number": {
                        "type": "integer",
                        "description": "The line number of the variable. Use the line numbers in the source code."
                    }
                },
                "required": ["line_number", "variable_name"],
                "strict": True,
                "additionalProperties": False,
                "parallel_tool_calls": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_api_documentation",
            "description": "Get the documentation of a specific API",
            "parameters": {
                "type": "object",
                "properties": {
                    "api_name": {
                        "type": "string",
                        "description": "Simple name of an API found in the source code. For example, if the API is imported as from sklearn.preprocessing import OneHotEncoder, only provide OneHotEncoder instead of sklearn.preprocessing.OneHotEncoder. The function is capable of resolving the fully qualified name.",
                    }
                },
                "required": ["name"],
                "strict": True,
                "additionalProperties": False,
                "parallel_tool_calls": False
            }
        }
    }
]
