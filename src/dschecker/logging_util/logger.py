import logging

level_map = {
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL
}

def setup_logger(name, level="info"):
    """
    Sets up a logger with a standard format

    Args:
        name (str): The name of the logger (usually __name__).
        level (str): The logging level (e.g., logging.INFO, logging.DEBUG).
            Default to logging.INFO

    Returs:
        logging.Logger: The configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level_map[level])

    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s\t%(module)s:\t%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
