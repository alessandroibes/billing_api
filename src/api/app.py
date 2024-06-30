import aioredis
import logging
import sys

from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.config import BaseConfig


def create_app():
    app = FastAPI(lifespan=lifespan)
    app.state.config = BaseConfig()
    
    __register_routers(app)
    __configure_logger(app)

    return app


def __register_routers(app: FastAPI):
    from api.presentation_layer.views.upload import router as boletos_router

    app.include_router(boletos_router)


def __configure_logger(app: FastAPI):
    logger = logging.getLogger("billing_api")
    logger.setLevel(app.state.config.LOGS_LEVEL)

    log_formatter = logging.Formatter("[%(levelname)s] %(asctime)s %(name)s: %(message)s")

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(log_formatter)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler('billing_api.log', mode='w')
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = await get_redis_client()
    yield
    await app.state.redis.close()


async def get_redis_client():
    config = BaseConfig()
    if config.TESTING:
        import fakeredis.aioredis
        redis = fakeredis.aioredis.FakeRedis()
    else:
        redis = aioredis.from_url(
            f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}", decode_responses=True
        )
    return redis