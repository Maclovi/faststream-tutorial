from faststream import FastStream, Logger
from faststream.rabbit import RabbitBroker

# Создаем брокер RabbitMQ
broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
# Создаем приложение FastStream
app = FastStream(broker)


# Подписываемся на очередь "input-queue"
@broker.subscriber("input-queue")
async def handle_message(msg: str, logger: Logger) -> None:
    logger.info(f"Получено сообщение: {msg}")
    # Отправляем результат в output-queue
    await broker.publish(f"Обработано: {msg.upper()}", queue="output-queue")


# Подписываемся на очередь "output-queue" для проверки результата
@broker.subscriber("output-queue")
async def check_result(msg: str, logger: Logger) -> None:
    logger.info(f"Результат: {msg}")
