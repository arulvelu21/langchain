import logging


def setup_logger(level=logging.INFO):
    """Basic logger setup for the application."""
    logger = logging.getLogger()
    if logger.handlers:
        # Avoid adding duplicate handlers during reloads
        return

    logger.setLevel(level)
    handler = logging.StreamHandler()
    fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(fmt)
    logger.addHandler(handler)

