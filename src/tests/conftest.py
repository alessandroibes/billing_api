import asyncio
import fakeredis.aioredis
import pytest
import sys
import os

from fastapi.testclient import TestClient

from api.app import create_app
from api.config import BaseConfig

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

app = create_app()


@pytest.fixture
async def fake_redis():
    config = BaseConfig()
    client = await fakeredis.aioredis.create_redis(
        f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}"
    )
    yield client
    client.close()
    await client.wait_closed()


@pytest.fixture
def client(fake_redis):    
    app.state.redis = fake_redis
    client = TestClient(app)
    yield client
    app.state.redis = None

