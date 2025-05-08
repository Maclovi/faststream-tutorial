from pydantic import BaseModel
from faststream import FastStream, Logger
from faststream.rabbit import RabbitBroker

# Определяем структуру сообщения
class UserMessage(BaseModel):
    username: str
    message: str


# Создаем брокер и приложение
broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
app = FastStream(broker)


# Подписываемся на очередь input-queue
@broker.subscriber("input-queue")
async def handle_message(data: UserMessage, logger: Logger) -> None:
    logger.info(f"Получено: {data.username} сказал '{data.message}'")
    # Отправляем результат в output-queue
    await broker.publish(
        UserMessage(username=data.username, message=data.message.upper()),
        queue="output-queue"
    )


# Подписываемся на очередь output-queue
@broker.subscriber("output-queue")
async def check_result(data: UserMessage, logger: Logger) -> None:
    logger.info(f"Промежуточный результат: {data.username} сказал '{data.message}'")
