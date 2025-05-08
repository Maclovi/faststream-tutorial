from faststream import FastStream, Logger
from faststream.rabbit import RabbitBroker

# Создаем брокер RabbitMQ
broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
# Создаем приложение FastStream
app = FastStream(broker)


# Подписчик: обрабатывает сообщения из final-queue
@broker.subscriber("final-queue")
async def final_result(msg: str, logger: Logger) -> None:
    logger.info(f"Финальный результат: {msg}")
