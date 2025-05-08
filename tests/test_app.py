import pytest
from unittest.mock import AsyncMock
from pydantic import BaseModel, ValidationError
from faststream.rabbit import RabbitBroker, TestBroker

# Определяем модель для тестов (копия из app.py)
class UserMessage(BaseModel):
    username: str
    message: str

@pytest.mark.asyncio
async def test_correct_message():
    # Создаем брокер
    broker = RabbitBroker()

    # Мокируем обработчики
    handle_message = AsyncMock()
    check_result = AsyncMock()

    @broker.subscriber("input-queue")
    async def handle_message_mock(data: UserMessage):
        await handle_message(data)
        await broker.publish(
            UserMessage(username=data.username, message=data.message.upper()),
            queue="output-queue"
        )

    @broker.subscriber("output-queue")
    async def check_result_mock(data: UserMessage):
        await check_result(data)

    # Тестируем с эмуляцией брокера
    async with TestBroker(broker):
        # Отправляем корректное сообщение
        await broker.publish(
            UserMessage(username="Alice", message="Hello"),
            queue="input-queue"
        )

        # Проверяем вызов handle_message
        handle_message.assert_called_once_with(UserMessage(username="Alice", message="Hello"))
        # Проверяем вызов check_result
        check_result.assert_called_once_with(UserMessage(username="Alice", message="HELLO"))

@pytest.mark.asyncio
async def test_invalid_message():
    broker = RabbitBroker()

    @broker.subscriber("input-queue")
    async def handle_message(data: UserMessage):
        pass

    # Тестируем с эмуляцией брокера
    async with TestBroker(broker):
        # Отправляем некорректное сообщение
        with pytest.raises(ValidationError):
            await broker.publish(
                {"username": "Alice", "wrong_field": "Hello"},
                queue="input-queue"
            )
