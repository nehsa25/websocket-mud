import logging
import os
from enum import Enum
from opentelemetry import trace, context

class Level(Enum):
    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

class LogUtils:
    @staticmethod
    def get_logger(filename, file_level, console_level, log_location, tracer=None):
        """Creates and configures a logger with file and console handlers.

        Args:
            filename (str): The name of the log file.
            file_level (Level): The logging level for the file handler (e.g., Level.DEBUG, Level.INFO).
            console_level (Level): The logging level for the console handler (e.g., Level.DEBUG, Level.INFO).
            log_location (str): The directory where the log file should be created.
            tracer: The OpenTelemetry tracer object.

        Returns:
            logging.Logger: The configured logger object.
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)  # Set the lowest level to DEBUG

        # Create file handler
        log_file_path = os.path.join(log_location, filename)
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(file_level.value)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level.value)

        # Create formatter and set it for handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    @staticmethod
    def debug(message, logger):
        """Logs a debug message with OpenTelemetry tracing."""
        LogUtils._log(message, logger, logging.DEBUG)

    @staticmethod
    def info(message, logger):
        """Logs an info message with OpenTelemetry tracing."""
        LogUtils._log(message, logger, logging.INFO)

    @staticmethod
    def warn(message, logger):
        """Logs a warning message with OpenTelemetry tracing."""
        LogUtils._log(message, logger, logging.WARNING)

    @staticmethod
    def error(message, logger):
        """Logs an error message with OpenTelemetry tracing."""
        LogUtils._log(message, logger, logging.ERROR)

    @staticmethod
    def critical(message, logger):
        """Logs a critical message with OpenTelemetry tracing."""
        LogUtils._log(message, logger, logging.CRITICAL)

    @staticmethod
    def _log(message, logger, level):
        """Logs a message with OpenTelemetry tracing."""
        if logger:
            tracer = trace.get_tracer(__name__)
            current_context = context.get_current()

            # Create span
            with tracer.start_as_current_span(message, context=current_context) as current_span:
                if current_span is not trace.INVALID_SPAN:
                    current_span.set_attribute("log.message", message)
                logger.log(level, message)