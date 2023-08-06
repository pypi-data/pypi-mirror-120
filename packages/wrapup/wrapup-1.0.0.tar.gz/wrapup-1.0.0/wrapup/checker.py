import ast


def checker(file_data: str, path: bool = True) -> bool:
    """Given a python file path/content, check whether the given file is syntactically correct or not

    Args:
        file_data: A path object or file content
        path: True if file path is passed instead of its content

    Return:
        True if the file/content is syntactically correct
    """
    try:
        if path:
            with open(file_data) as f:
                source = f.read()
        else:
            source = file_data
        ast.parse(source)
        return True
    except SyntaxError:
        return False
    except Exception:
        return False
