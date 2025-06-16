import logging
import sys

formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger = logging.getLogger("sfm")
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger.propagate = False
