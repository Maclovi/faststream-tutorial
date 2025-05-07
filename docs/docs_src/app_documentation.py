from pydantic import BaseModel, Field
from faststream import FastStream, Logger
from faststream.rabbit import RabbitBroker


class UserMessage(BaseModel):
    username: str = Field(examples=["Alice"], description="Имя пользователя")
    message: str = Field(examples=["Hello"], description="Текст сообщения")

broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
app = FastStream(
    broker,
    title="Мое первое FastStream-приложение",
    description="Приложение для обработки сообщений пользователей через RabbitMQ"
)


@broker.subscriber("input-queue")
async def handle_message(data: UserMessage, logger: Logger) -> None:
    """Обрабатывает входящее сообщение и отправляет результат в output-queue."""
    logger.info(f"Получено: {data.username} сказал '{data.message}'")
    await broker.publish(
        UserMessage(username=data.username, message=data.message.upper()),
        queue="output-queue"
    )


@broker.subscriber("output-queue")
async def check_result(data: UserMessage, logger: Logger) -> None:
    """Проверяет обработанное сообщение из output-queue."""
    logger.info(f"Результат: {data.username} сказал '{data.message}'")
