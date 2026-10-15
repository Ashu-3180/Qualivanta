"""Small, configurable logging setup for framework modules."""

from __future__ import annotations

import logging
import os


def get_logger(name: str = "qualivanta") -> logging.Logger:
    """Return a consistently formatted logger without duplicating handlers."""

    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
        logger.addHandler(handler)
        logger.propagate = False
    logger.setLevel(os.environ.get("QUALIVANTA_LOG_LEVEL", "INFO").upper())
    return logger
