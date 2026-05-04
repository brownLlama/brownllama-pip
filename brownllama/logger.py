"""
Drop-in Loguru logger that also captures stdlib logging from third-party libs.

Usage:
    from brownlog import logger
    logger.info("Test")
"""

import logging
import sys

from loguru import logger


class _InterceptHandler(logging.Handler):
    """Redirect all stdlib logging into Loguru."""

    def emit(self, record: logging.LogRecord) -> None:
        # Get the corresponding Loguru level
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find the correct caller frame so Loguru shows the right origin
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            self.format(record),  # ← use self.format() to silence the linter
        )


# Route all stdlib logging (third-party libs) into Loguru - runs once on import
logging.basicConfig(handlers=[_InterceptHandler()], level=0, force=True)


__all__ = ["logger"]
