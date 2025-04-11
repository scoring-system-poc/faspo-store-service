import logging
import logging.config
import azure.monitor.opentelemetry

from src.core.config import CONFIG


def setup_logging():
    """
    Set up logging configuration.
    """
    azure.monitor.opentelemetry.configure_azure_monitor(logger_name="src")

    logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.WARNING)

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation-id-filter": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": 16,
                    "default_value": "0" * 16,
                },
            },
            "formatters": {
                "stdout-fmt": {
                    "class": "logging.Formatter",
                    "format": "%(asctime)s | %(levelname)-7s | %(name)-20s | %(funcName)-20s | %(correlation_id)-16s | %(message)s",
                },
            },
            "handlers": {
                "stdout-handler": {
                    "class": "logging.StreamHandler",
                    "filters": ["correlation-id-filter"],
                    "formatter": "stdout-fmt",
                },
            },
            "root": {"handlers": ["stdout-handler"], "level": CONFIG.LOG_LEVEL},
        }
    )

