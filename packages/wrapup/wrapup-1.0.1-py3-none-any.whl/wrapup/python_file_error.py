class NotAPythonFile(Exception):
    """Exception raised when a given file is not a python file"""

    def __init__(self, path) -> None:
        self.path = path
        self.message = self.path.name + " is not a python file."
        super().__init__(self.message)
