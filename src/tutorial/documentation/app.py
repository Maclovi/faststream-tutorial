from pydantic import BaseModel, Field
from faststream import FastStream, Logger
from faststream.rabbit import RabbitBroker

# Определяем структуру сообщения с метаданными
class UserMessage(BaseModel):
    username: str = Field(description="Имя пользователя", examples=["Alice"])
    message: str = Field(description="Текст сообщения", examples=["Hello"])


# Создаем брокер и приложение с метаданными
broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
app = FastStream(broker,
    title="User Message Processor",
    description="Приложение для обработки пользовательских сообщений",
)


# Подписываемся на очередь input-queue
@broker.subscriber("input-queue")
async def handle_message(data: UserMessage, logger: Logger) -> None:
    """
    Принимает сообщение из input-queue, логирует его и
    отправляет в output-queue с текстом в верхнем регистре.
    """
    logger.info(f"Получено: {data.username} сказал '{data.message}'")
    await broker.publish(
        UserMessage(username=data.username, message=data.message.upper()),
        queue="output-queue"
    )


# Подписываемся на очередь output-queue
@broker.subscriber("output-queue")
async def check_result(data: UserMessage, logger: Logger) -> None:
    """Логирует обработанное сообщение из output-queue."""
    logger.info(f"Промежуточный результат: {data.username} сказал '{data.message}'")
