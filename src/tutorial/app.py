from faststream import FastStream, Logger
from faststream.rabbit import RabbitBroker

# Создаем брокер RabbitMQ
broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
# Создаем приложение FastStream
app = FastStream(broker)


# Подписываемся на очередь "input-queue" и публикуем в "output-queue"
@broker.subscriber("input-queue")
@broker.publisher("output-queue")
async def handle_message(msg: str, logger: Logger) -> str:
    logger.info(f"Получено сообщение: {msg}")
    return f"Обработано: {msg.upper()}"
