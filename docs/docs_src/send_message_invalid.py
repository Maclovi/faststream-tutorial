import asyncio
from faststream.rabbit import RabbitBroker


async def send_message():
    async with RabbitBroker("amqp://guest:guest@localhost:5672/") as broker:
        await broker.publish(
            {"username": "Alice", "wrong_field": "Hello"},  # Неверное поле
            queue="input-queue"
        )


if __name__ == "__main__":
    asyncio.run(send_message())
