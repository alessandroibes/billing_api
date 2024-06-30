import logging
import os


class BaseConfig():
    LOGS_LEVEL = logging.INFO
    REDIS_HOST = "redis"
    REDIS_PORT = "6379"
    TESTING: bool = os.getenv("TESTING", "0") == "1"
