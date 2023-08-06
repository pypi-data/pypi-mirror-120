import re
from pathlib import Path

# Local modules
try:
    from .checker import checker
except ImportError:
    from checker import checker

try:
    from .helpers import checkBrackets
except ImportError:
    from helpers import checkBrackets


###################### REGULAR EXPRESSIONS ######################

skip_a_line = re.compile(r".*")  # Skipping a line (upto the newline character)
multiline_comments = re.compile(
    r"""('''|\"\"\") 
        (.*?) # Any number of lines between the comments including newline characters
        ('''|\"\"\")""",
    re.DOTALL | re.VERBOSE,
)
# Regex checking for a whole print statement
print_checker = re.compile(r"([ \t]*print)(\(.*\))([ \t]*)", re.DOTALL)

comments = re.compile(r"[ \t]*(#|'''|\"\"\")")
hash_comments = re.compile(r"[ \t]*#")

# To check if mulitiline comments start from here
multiline_comments_start_spc = re.compile(r"[ \t]*('''|\"\"\")")

# For checking a whole multiline comment
multiline_comments_spc = re.compile(r"[ \t]*('''.*'''|\"\"\".*\"\"\")[ \t]*", re.DOTALL)
blank_line = re.compile(r"^[ \t]*$")
re_indentation = re.compile(r"([ \t]+)(.)")
#################################################################


def convert_quotes_slave(filepath: Path, single: bool = True) -> bool:
    """
    Helper function to convert the quotes in file

    Args:
        filepath: A path object pointing to path of the file to convert
        single: A boolean value signifying True if convert quotes to single quotes and False for double quotes

    Returns:
        True if the file is converted to desired quotes without any syntactitcal errors
    """

    # Opening the file and checking for any syntactical errors
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = file.read()
            if not checker(data, False):
                return (False, filepath)
    except UnicodeDecodeError:
        return (False, filepath)

    # Desired quotes in the file
    dest = "'" if single else '"'
    new_file_content = ""
    quotes = ('"', "'")
    i = 0
    while i < len(data):

        # If a hashed comment occurs, no need to check the comment string for quotes
        if data[i] == "#":
            hashed_comment = re.match(skip_a_line, data[i:])
            new_file_content += data[i : i + hashed_comment.span()[1]]
            # Skip the characters in the comment upto newline
            i = i + hashed_comment.span()[1]

        # Main condition: If a quote is encountered
        elif data[i] in quotes:

            # Check if it is a docstring
            matched_comments = re.match(multiline_comments, data[i:])
            if matched_comments:
                # Replacing the docstring quotes with the desired quotes
                new_file_content += dest * 3 + matched_comments.group(2) + dest * 3
                i += matched_comments.span()[1]  # Skip the docstring

            else:
                ends = data[i]  # Start of the string
                new_file_content += dest  # Replace the quote with the  desired quote
                i += 1

                # Go upto the end of string
                while data[i] != ends:

                    # This condition is used so that we do not check the escape character
                    # Mainly used for these cases:
                    # i) If the next character is a backslash
                    # ii) If the next character is a quote
                    if data[i] == "\\":
                        new_file_content += data[i]
                        i += 1

                    # If a destination quote occurs in the string escape it
                    elif data[i] == dest:
                        new_file_content += "\\"

                    new_file_content += data[i]
                    i += 1

                new_file_content += dest  # Close the string
                i += 1

        if i < len(data):
            new_file_content += data[i]

        i += 1
    # Check the result if it contains any syntactical errors
    if checker(new_file_content, False):
        try:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(new_file_content)
        except UnicodeEncodeError:
            return (False, filepath)
        return (True, filepath)
    else:
        return (False, filepath)


def rmv_prints_slave(
    filepath: Path,
    rmv_main: bool = True,
    rmv_root: bool = True,
    funcs_to_spare: list = None,
) -> int:
    """
    Function which will change the file and remove print statements from print

    Args:
        filepath: A path object pointing to path of the file
        rmv_main: True if print statements has to be removed from main function else False
        rmv_root: True if print statements has to be removed from global scope (level 0 indentation) else False
        funcs_to_spare: List of functions to be ignored in a file

    Return:
        An integer which has the following cases:
        0: Print statements could not be removed due to syntactical errors
        1: Print statements were removed from the file successfully
        2: There were no print statements in the file hence, no change

    """

    if funcs_to_spare == None:
        funcs_to_spare = list()

    # main() is used by many programmers, so for standard puposes we do this
    if rmv_main == False:
        funcs_to_spare.append("main")

    there_are_functions_to_spare = True

    if len(funcs_to_spare) == 0:
        there_are_functions_to_spare = False
    else:
        # Get a string in the form of "(func 1|func 2|func 3|....|func n)" to be used in the regex
        function_identifiers = "("
        for i in range(len(funcs_to_spare)):
            function_identifiers += funcs_to_spare[i] + "|"
        function_identifiers = function_identifiers[0:-1] + ")"

    if rmv_main == False:
        re_spare_funcs = re.compile(
            r"(if(\(|\s)*__name__\s*==\s*('|\")__main__('|\")(\)|\s)*:)|([ \t]*def[ ]+"
            + function_identifiers
            + r"\s*\(.*\).*?:)",
        )

    elif there_are_functions_to_spare:
        re_spare_funcs = re.compile(
            r"[ \t]*def[ ]+" + function_identifiers + r"\s*\(.*\).*?:"
        )

    if rmv_root == True:
        line_contains_print = re.compile(r"[ \t]*print\(")
    else:
        line_contains_print = re.compile(r"[ \t]+print\(")

    # Opening the file and checking for any syntactical errors
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = file.readlines()
            if not checker(filepath, True):
                return (0, filepath)
    except UnicodeDecodeError:
        return (0, filepath)

    current_line = 0
    lines_in_file = len(data)
    new_file_content = ""
    change = False  # A variable to know if there were any print statements in file
    while current_line < len(data):
        # If any comment is encountered
        if re.match(comments, data[current_line]):

            # Go through the multiline docstring until its end
            if re.match(multiline_comments_start_spc, data[current_line]):
                end = current_line
                cur_comment = data[current_line]
                while not re.match(multiline_comments_spc, cur_comment):
                    end += 1
                    cur_comment += data[end]
                new_file_content += cur_comment
                current_line = end
            else:
                new_file_content += data[current_line]

        # If a function definition is encountered and it is a function to be ignored for checking of print statements, skip it
        elif there_are_functions_to_spare and re.match(
            re_spare_funcs, data[current_line]
        ):
            function_end = re.match(re_spare_funcs, data[current_line]).span()[1]
            # Check whether this is not a one-line function
            # eg. def a(b): return b*3
            if function_end == len(data[current_line]) or re.match(
                blank_line, data[current_line][function_end:]
            ):
                # In function body, skip the blank lines and comments to find the indentation of the function
                end = current_line + 1
                while end < lines_in_file and (
                    re.match(hash_comments, data[end])
                    or re.match(blank_line, data[end])
                ):
                    end += 1
                if end < lines_in_file:
                    # First ordinary line of function, get the indentation level
                    indentation = re.match(re_indentation, data[end])
                    no_of_spaces = len(indentation.group(1))
                    block_text = re.compile(r"[ \t]{" + str(no_of_spaces) + r",}.")
                    # Go through the function with the at least the current indentation
                    while end < lines_in_file and (
                        re.match(hash_comments, data[end])
                        or re.match(blank_line, data[end])
                        or re.match(block_text, data[end])
                    ):
                        end += 1
                new_file_content += "".join(data[current_line:end])
                current_line = end - 1

        # If a print statement is encountered, remove it
        elif re.match(line_contains_print, data[current_line]):
            # Print statement is encountered hence, file needs to be changed
            change = True
            end = current_line
            print_statement = re.match(print_checker, data[current_line])
            current_print = data[current_line]

            # If the print statement is incomplete or a matching bracket is found in the statement,
            # check if the print statement is complete
            while end < lines_in_file and (
                print_statement == None
                or checkBrackets(print_statement.group(2)) == False
            ):
                end += 1
                current_print += data[end]
                print_statement = re.match(print_checker, current_print)
            current_line = end

        # If all of the above cases are not true, this is a regular line just append it to the file content
        else:
            new_file_content += data[current_line]

        current_line += 1

    if checker(new_file_content, False):
        # No print in the file was noticed, hence no need to write anything to the file
        if not change:
            return (2, filepath)
        try:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(new_file_content)
        except UnicodeEncodeError:
            return (0, filepath)
        return (1, filepath)
    else:
        return (0, filepath)


if __name__ == "__main__":
    convert_quotes_slave(
        "C:/Users/DELL/OneDrive/Desktop/wrapup/wrapup/filepath.py",
        single=False,
    )
