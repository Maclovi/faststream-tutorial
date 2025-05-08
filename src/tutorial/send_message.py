import asyncio
from faststream.rabbit import RabbitBroker


async def send_message(broker: RabitBroker) -> None:
    await broker.publish("Привет, FastStream!", queue="input-queue")


async def main() -> None:
    async with RabbitBroker("amqp://guest:guest@localhost:5672/") as broker:
        await send_message(broker)


if __name__ == "__main__":
    asyncio.run(main())
