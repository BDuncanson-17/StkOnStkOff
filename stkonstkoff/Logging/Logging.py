class ErrorHandler:
    """
    Class for handling errors and generating error messages.
    """

    def __init__(self):
        pass

    @staticmethod
    def handle_error(message):
        """
        Handles an error and returns an error message string.
        Args:
            message (str): The error message.
        Returns:
            str: The formatted error message string.
        """
        return f"[ERROR] {message}"


class Logger:
    """
    Class for logging messages with different log levels.
    """

    def __init__(self):
        pass

    @staticmethod
    def log_info(message):
        """
        Log a message with the info level and return the formatted log string.
        Args:
            message (str): The log message.
        Returns:
            str: The formatted info log string.
        """
        return f"[INFO] {message}"

    @staticmethod
    def log_warning(message):
        """
        Log a message with the warning level and return the formatted log string.
        Args:
            message (str): The log message.
        Returns:
            str: The formatted warning log string.
        """
        return f"[WARNING] {message}"

    @staticmethod
    def log_error(message):
        """
        Log a message with the error level and return the formatted log string.
        Args:
            message (str): The log message.
        Returns:
            str: The formatted error log string.
        """
        return f"[ERROR] {message}"

