import asyncio
from faststream.rabbit import RabbitBroker


async def send_message(broker: RabbitBroker) -> None:
    await broker.publish(
        {"username": "Alice", "wrong_field": "Hello"},  # Неверное поле
        queue="input-queue"
    )


async def main() -> None:
    async with RabbitBroker("amqp://guest:guest@localhost:5672/") as broker:
        await send_message(broker)


if __name__ == "__main__":
    asyncio.run(main())
