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
    logger.info(f"Обработано: {msg.upper()}")
