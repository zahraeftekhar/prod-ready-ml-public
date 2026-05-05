import logging


def setup_logger(*, level: int = logging.INFO) -> None:
    """Set up the logger for the application.

    Args:
        level (int): The logging level to set. Defaults to
            `logging.INFO`.
    """
    logger = logging.getLogger("animal_shelter")

    # Avoid adding duplicate handlers
    if logger.handlers:
        logger.handlers.clear()

    logger.setLevel(level)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


def set_log_level(level: int | str) -> None:
    """Set the logging level for the application. This is used for runtime configuration of the logger.
    updates both the logger and its handlers. We call this during execusion to change verbosity without reinitializing the logger.

    Args:
        level (int | str): The logging level to set. Can be an integer (e.g., `logging.DEBUG`) or a string (e.g., "DEBUG").
    """
    logger = logging.getLogger("animal_shelter")
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)

# Initialize logger when module is imported (default to INFO level)
setup_logger(level=logging.INFO)
# set_log_level(logging.WARNING)
