import os
from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from faststream.rabbit import RabbitBroker, TestRabbitBroker
from pydantic import ValidationError

from app import UserMessage, check_result, handle_message
from app import broker as broker_app1

WITH_REAL = os.getenv("TEST_BROKER_WITH_REAL", False) == "1"


@pytest_asyncio.fixture(scope="module")
async def client_broker1() -> AsyncIterator[RabbitBroker]:
    async with TestRabbitBroker(broker_app1, with_real=WITH_REAL) as br_client:
        yield br_client


@pytest.mark.asyncio
async def test_correct_message_app1(client_broker1: RabbitBroker) -> None:
    await client_broker1.publish(
        UserMessage(username="Alice", message="Hello"), queue="input-queue"
    )
    # Проверяем вызов handle_message (app.py)
    handle_message.mock.assert_called_once_with(
        {"username": "Alice", "message": "Hello"}
    )
    # Проверяем вызов check_result (app.py)
    check_result.mock.assert_called_once_with({"username": "Alice", "message": "HELLO"})


@pytest.mark.asyncio
async def test_invalid_message(client_broker1: RabbitBroker) -> None:
    with pytest.raises(ValidationError):
        await client_broker1.publish(
            {"username": "Alice", "wrong_field": "Hello"}, queue="input-queue"
        )
