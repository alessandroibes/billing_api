import logging
import os


class BaseConfig():
    LOGS_LEVEL = logging.INFO
    REDIS_HOST = "localhost"
    REDIS_PORT = "16379"
    TESTING: bool = os.getenv("TESTING", "0") == "1"
