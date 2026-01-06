import sys
import os
from loguru import logger
from utils.ui.config_reader import get_log_to_file, get_log_file_path

# Configure loguru to match the emoji format
logger.remove()  # Remove default handler

# Set custom icon for INFO level
logger.level("INFO", icon="ℹ️")

# Add console handler with emoji format
logger.add(
    sys.stderr,
    format="{time} - ℹ️ - INFO - {message}",
    level="INFO",
    colorize=True
)

# Add file handler if configured (keeping the config integration)
try:
    if get_log_to_file():

        log_file_path = get_log_file_path()
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        logger.add(log_file_path, format="{time} - INFO - {message}", level="INFO")
except ImportError:
    pass

def printf(*args, sep=" "):
    """Logging function using loguru that accepts multiple arguments like print."""
    msg = sep.join(str(a) for a in args)
    logger.info(msg)