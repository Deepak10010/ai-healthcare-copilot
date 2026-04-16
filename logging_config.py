import logging
import time

from config import settings


def setup_logging():
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


class PipelineTimer:
    """Context manager for timing pipeline stages."""

    def __init__(self, stage_name: str, logger: logging.Logger):
        self.stage_name = stage_name
        self.logger = logger
        self.elapsed = 0.0

    def __enter__(self):
        self.start = time.time()
        self.logger.info(f"Starting: {self.stage_name}")
        return self

    def __exit__(self, *args):
        self.elapsed = time.time() - self.start
        self.logger.info(f"Completed: {self.stage_name} ({self.elapsed:.2f}s)")
