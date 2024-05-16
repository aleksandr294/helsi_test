"""
Module for setting up and using a logger with Loguru.
This module configures a logger for logging messages using Loguru
and exports the logger object for use from other modules.
"""

from loguru import logger
import sys

logger.add(
    sys.stdout,
    level="INFO",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
)

app_logger = logger
