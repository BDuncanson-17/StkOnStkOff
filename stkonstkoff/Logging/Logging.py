
from datetime import datetime

# Get the current time
class ErrorHandler:
    """
    Class for handling errors and generating error messages.
    """

    def __init__(self):
        self.error_messages = [
            'Unknown Error'
            'Object error'
        ]
        self.type = ["[Error]" "[Info]" "[Warning]"]





    @staticmethod
    def handle_error(error_number=0):
        """
        Handles an error and returns an error message string.
        Args:
            message (str): The error message.
        Returns:
            str: The formatted error message string.
        """
        return f"[ERROR]\t{datetime.now(tz='cst')}\t{ErrorHandler.Error_Message[error_number]}"


class Logger:
    """
    Class for logging messages with different log levels.
    """

    def __init__(self):
        pass

    @staticmethod
    def Log(error_type=0,message=0):
        """
        Log a message with the info level and return the formatted log string.
        Args:
            message (str): The log message.
        Returns:
            str: The formatted info log string.
        """
        return f"{ErrorHandler.ErrorType[error_type]} {ErrorHandler.ErrorMessage[message]}"

