import os
from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from faststream.rabbit import RabbitBroker, TestRabbitBroker

from app2 import broker as broker_app2
from app2 import final_result

WITH_REAL = os.getenv("TEST_BROKER_WITH_REAL", False) == "1"


@pytest_asyncio.fixture(scope="module")
async def client_broker2() -> AsyncIterator[RabbitBroker]:
    async with TestRabbitBroker(broker_app2, with_real=WITH_REAL) as br_client:
        yield br_client


@pytest.mark.asyncio
async def test_correct_message_app2(client_broker2: RabbitBroker) -> None:
    await client_broker2.publish("Привет, FastStream!", queue="final-queue")
    # Проверяем вызов final_result (app2.py)
    final_result.mock.assert_called_once_with("Привет, FastStream!")
