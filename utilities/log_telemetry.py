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
    @staticmethod
    def get_logger(
        filename="mud.log",
        file_level=GlobalSettings.FILE_LEVEL,
        console_level=GlobalSettings.CONSOLE_LEVEL,
        log_location=GlobalSettings.LOG_LOCATION,
        tracer=None,
    ):
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
        logger.setLevel(logging.DEBUG)

        if log_location is None:
            log_location = os.getcwd()

        if tracer is None:
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
                logger.error(f"Error initializing OTLP Exporter: {e}", logger)
                otlp_exporter = None

            if otlp_exporter:
                tracer_provider = TracerProvider(resource=resource)

                # Add ConsoleSpanExporter to see spans in the console
                tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
                tracer_provider.add_span_processor(
                    BatchSpanProcessor(ConsoleSpanExporter())
                )
                trace.set_tracer_provider(tracer_provider)
                tracer = trace.get_tracer(__name__)

        # Create file handler
        log_file_path = os.path.join(log_location, filename)
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(file_level.value)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level.value)

        # Create formatter and set it for handlers
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    @staticmethod
    def debug(message, logger):
        """Logs a debug message with OpenTelemetry tracing."""
        LogTelemetryUtility._log(message, logger, logging.DEBUG)

    @staticmethod
    def info(message, logger):
        """Logs an info message with OpenTelemetry tracing."""
        LogTelemetryUtility._log(message, logger, logging.INFO)

    @staticmethod
    def warn(message, logger):
        """Logs a warning message with OpenTelemetry tracing."""
        LogTelemetryUtility._log(message, logger, logging.WARNING)

    @staticmethod
    def error(message, logger):
        """Logs an error message with OpenTelemetry tracing."""
        LogTelemetryUtility._log(message, logger, logging.ERROR)

    @staticmethod
    def critical(message, logger):
        """Logs a critical message with OpenTelemetry tracing."""
        LogTelemetryUtility._log(message, logger, logging.CRITICAL)

    @staticmethod
    def _log(message, logger, level):
        """Logs a message with OpenTelemetry tracing."""
        if logger:
            tracer = trace.get_tracer(__name__)
            current_context = context.get_current()

            # Create span
            with tracer.start_as_current_span(
                message, context=current_context
            ) as current_span:
                if current_span is not trace.INVALID_SPAN:
                    current_span.set_attribute("log.message", message)
                logger.log(level, message)
