def skipString(s: str, st_idx: int) -> int:
    """Used to skip an str object in a python print statement taken from a file

    Args:
        s: An str object which needs to be traversed
        st_idx: Start index for the str object

    Return:
        The end index of the str object
    """
    i = st_idx + 1
    # This loop traverse through the string and ignores the next character to backslash character
    while i < len(s) and (s[i] != s[st_idx] or s[i - 1] == "\\"):
        i += 1
    return i


def checkBrackets(s: str) -> bool:
    """Check the brackets in a print statement to check if it is complete or not

    Args:
        s: An str object

    Return:
        True if the statement is complete else False
    """
    i = 0
    open = 0
    # Loop to check the opening and closing bracket consistencies
    while i < len(s):
        if s[i] == "(":
            open += 1
        elif s[i] == ")":
            if open <= 0:
                return False
            open -= 1
        # If any string starts skip it, as it may contain brackets
        elif s[i] == "'" or s[i] == '"':
            i = skipString(s, i)
        i += 1
    return open == 0
