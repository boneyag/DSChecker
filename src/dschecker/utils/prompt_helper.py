def add_line_numbers_to_code(code):
    numbered_code_array = []

    if isinstance(code, str):
        for num, line in enumerate(code.split("\n")):
            numbered_code_array.append(f"{num+1}\t{line}")
    if isinstance(code, list):
        for num, line in enumerate(code):
            numbered_code_array.append(f"{num+1}\t{line}")

    return numbered_code_array
