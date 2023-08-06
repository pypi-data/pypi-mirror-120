from pathlib import Path


def getfilepath(filename: str) -> Path:
    """
    Searches for the filepath in the current directory and parent directory
    If an empty string or nothing is passed as the parameter, sets the current working directory as path
    Args:
        filename: An str object that represents a file or a folder path
    Return:
        Path to the file object
    """
    filepath = None
    if not filename:
        filepath = Path(__file__).parent
    else:
        filepath = Path(filename)
        if not filepath.exists():
            check_in_parent = Path(__file__).parent / filename
            if not check_in_parent.exists():
                raise FileNotFoundError
            else:
                filepath = check_in_parent
    return filepath
