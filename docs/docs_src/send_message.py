import asyncio
from faststream.rabbit import RabbitBroker


async def send_message() -> None:
    async with RabbitBroker("amqp://guest:guest@localhost:5672/") as broker:
        await broker.publish("Привет, FastStream!", queue="input-queue")


if __name__ == "__main__":
    asyncio.run(send_message())
