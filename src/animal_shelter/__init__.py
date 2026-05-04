# def main() -> None:
#     print("Hello from animal-shelter!")


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


# Initialize logger when module is imported (default to INFO level)
setup_logger(level=logging.INFO)


def set_log_level(level: int | str) -> None:
    logger = logging.getLogger("animal_shelter")
    logger.setLevel(level)
    for h in logger.handlers:
        h.setLevel(level)


# Implement your own logger.setLevel()
