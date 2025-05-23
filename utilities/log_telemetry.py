import inspect
import logging
import os
from opentelemetry import trace, context
from dontcheckin import Secrets

# OpenTelemetry imports
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes
from opentelemetry.sdk.trace.export import ConsoleSpanExporter

from settings.global_settings import GlobalSettings


class LogTelemetryUtility:
    def __init__(
        self,
        logger_name="mud",
        filename="logs/mud.log",
        file_level=GlobalSettings.FILE_LEVEL,
        console_level=GlobalSettings.CONSOLE_LEVEL,
        log_location=GlobalSettings.LOG_LOCATION,
    ):
        """Creates and configures a logger with file and console handlers.

        Args:
            filename (str): The name of the log file.
            file_level (Level): The logging level for the file handler (e.g., Level.DEBUG, Level.INFO).
            console_level (Level): The logging level for the console handler (e.g., Level.DEBUG, Level.INFO).
            log_location (str): The directory where the log file should be created.
        """
        self.logger = logging.getLogger(__name__)  if logger_name == "" else logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.filename = filename
        self.file_level = file_level
        self.console_level = console_level
        self.log_location = log_location
        self.tracer = None

        if self.log_location is None:
            self.log_location = os.getcwd()

        # Initialize OpenTelemetry
        resource = Resource.create(
            {
                ResourceAttributes.SERVICE_NAME: "websocket-mud",
                ResourceAttributes.SERVICE_VERSION: "0.1.0",
            }
        )

        seq_api_key = Secrets.SeqAPIKey
        headers = {
            "X-Seq-ApiKey": seq_api_key,
            "Content-Type": "application/x-protobuf",
        }
        try:
            otlp_exporter = OTLPSpanExporter(
                endpoint="http://util.nehsa.net:5341/ingest/otlp/v1/traces",
                headers=headers,
            )

        except Exception as e:
            self.logger.error(f"Error initializing OTLP Exporter: {e}")
            otlp_exporter = None

        if otlp_exporter:
            tracer_provider = TracerProvider(resource=resource)

            # Add ConsoleSpanExporter to see spans in the console
            tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
            tracer_provider.add_span_processor(
                BatchSpanProcessor(ConsoleSpanExporter())
            )
            trace.set_tracer_provider(tracer_provider)
            self.tracer = trace.get_tracer(__name__)

        # Create file handler
        log_file_path = os.path.join(self.log_location, self.filename)
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(self.file_level.value)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.console_level.value)

        # Create formatter and set it for handlers
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, message):
        """Logs a debug message with OpenTelemetry tracing."""
        self._log(message, logging.DEBUG)

    def info(self, message):
        """Logs an info message with OpenTelemetry tracing."""
        self._log(message, logging.INFO)

    def warn(self, message):
        """Logs a warning message with OpenTelemetry tracing."""
        self._log(message, logging.WARNING)

    def error(self, message):
        """Logs an error message with OpenTelemetry tracing."""
        self._log(message, logging.ERROR)

    def critical(self, message):
        """Logs a critical message with OpenTelemetry tracing."""
        self._log(message, logging.CRITICAL)

    def _log(self, message, level):
        """Logs a message with OpenTelemetry tracing."""
        if self.logger:
            current_context = context.get_current()

            frame = inspect.currentframe().f_back.f_back

            lineno = frame.f_lineno
            method_name = frame.f_code.co_name

            # Create span
            with self.tracer.start_as_current_span(
                message, context=current_context
            ) as current_span:
                if current_span is not trace.INVALID_SPAN:
                    current_span.set_attribute("log.message", message)
                    current_span.set_attribute("log.line_number", lineno)
                    current_span.set_attribute("log.method", method_name)
                    current_span.set_attribute("log.level", level)
                    current_span.set_attribute("log.logger_name", self.logger.name)
                self.logger.log(level, message)

    @staticmethod
    def get_logger(
        logger_name="mud",
        filename="logs/mud.log",
        file_level=GlobalSettings.FILE_LEVEL,
        console_level=GlobalSettings.CONSOLE_LEVEL,
        log_location=GlobalSettings.LOG_LOCATION,
    ):
        """Creates and configures a logger with file and console handlers.

        Args:
            filename (str): The name of the log file.
            file_level (Level): The logging level for the file handler (e.g., Level.DEBUG, Level.INFO).
            console_level (Level): The logging level for the console handler (e.g., Level.DEBUG, Level.INFO).
            log_location (str): The directory where the log file should be created.

        Returns:
            logging.Logger: The configured logger object.
        """

        
        return LogTelemetryUtility(logger_name, filename, file_level, console_level, log_location)
