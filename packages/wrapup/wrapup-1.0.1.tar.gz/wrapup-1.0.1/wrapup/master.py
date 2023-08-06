from typing import List
import multiprocessing as mp

try:
    from .filepath import getfilepath
except ImportError:
    from filepath import getfilepath

try:
    from . import workers
except ImportError:
    import workers

try:
    from .python_file_error import NotAPythonFile
except:
    from python_file_error import NotAPythonFile


def rmv_print(
    filename: str = None,
    rmv_main: bool = False,
    rmv_root: bool = False,
    funcs_to_spare: list = None,
) -> List[str]:
    """
    Function which will traverse the file(s) from the given file/folder path and remove print statements from python files

    Args:
        filepath: A string specifying the path of a file/folder
        rmv_main: True if print statements has to be removed from main function else False
        rmv_root: True if print statements has to be removed from global scope (level 0 indentation) else False
        funcs_to_spare: List of functions to be ignored in a file

    Returns:
        List containing path of python files to which changes were done
    """
    filepath = getfilepath(filename)
    changes = list()  # List containing files to which changes were done
    if filepath.is_file():
        if filepath.suffix == ".py":
            result = workers.rmv_prints_slave(
                filepath, rmv_main, rmv_root, funcs_to_spare
            )
            if result[0] == 1:
                changes.append(str(result[1]))
        else:
            raise NotAPythonFile(filepath)
    else:
        python_files = [
            path
            for path in sorted(filepath.rglob("*"))
            if path.is_file() and path.suffix == ".py"
        ]

        def collect_result(result):
            """This is a callback function for apply_async function"""
            nonlocal changes
            # Changes were applied to the files
            if result[0] == 1:
                changes.append(str(result[1]))

        pool = mp.Pool(mp.cpu_count())
        for file in python_files:
            pool.apply_async(
                workers.rmv_prints_slave,
                args=(file, rmv_main, rmv_root, funcs_to_spare),
                callback=collect_result,
            )
        pool.close()
        pool.join()  # postpones the execution of next line of code until all processes in the queue are done

        changes.sort()

    return changes


def convert_quotes(filename: str, single: bool = True) -> List[str]:
    """
    Function to convert the quotes from python file(s) for the given file/folder path

    Args:
        filepath: A string specifying the path of a file/folder
        single: A boolean value which is True if quotes are to be converted to single
                quotes and False for double quotes

    Returns:
        List containing path of python files to which changes were done
    """
    filepath = getfilepath(filename)
    changes = list()  # List containing files to which changes were done

    # No need for multiprocessing
    if filepath.is_file():
        if filepath.suffix == ".py":
            result = workers.convert_quotes_slave(filepath=filepath, single=single)
            if result[0]:
                changes.append(str(result[1]))
        else:
            raise NotAPythonFile(filepath)
    else:
        python_files = [
            path
            for path in sorted(filepath.rglob("*"))
            if path.is_file() and path.suffix == ".py"
        ]

        def collect_result(result):
            nonlocal changes
            if result[0]:
                changes.append(str(result[1]))

        pool = mp.Pool(mp.cpu_count())
        for file in python_files:
            pool.apply_async(
                workers.convert_quotes_slave,
                args=(file, single),
                callback=collect_result,
            )
        pool.close()
        pool.join()  # postpones the execution of next line of code until all processes in the queue are done

        changes.sort()
    return changes


if __name__ == "__main__":
    rmv_print(
        filename="C:\\Users\\DELL\\OneDrive\\Desktop\\wrapup\\wrapup\\filepath.py",
        funcs_to_spare=[],
    )
