import asyncio

from faststream.rabbit import RabbitBroker
from pydantic import BaseModel


class UserMessage(BaseModel):
    username: str
    message: str


async def send_message(broker: RabbitBroker) -> None:
    message = UserMessage(username="Alice", message="Hello")
    await broker.publish(message, queue="input-queue")


async def main() -> None:
    async with RabbitBroker("amqp://guest:guest@localhost:5672/") as broker:
        await send_message(broker)


if __name__ == "__main__":
    asyncio.run(main())
