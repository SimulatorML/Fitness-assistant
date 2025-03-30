import logging
import sys

def setup_logging(level: int = logging.INFO):
    """Set up centralized logging configuration."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )
