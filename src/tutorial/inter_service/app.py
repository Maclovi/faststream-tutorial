from faststream import FastStream, Logger
from faststream.rabbit import RabbitBroker

# Создаем брокер RabbitMQ
broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
# Создаем приложение FastStream
app = FastStream(broker)


# Первый подписчик: обрабатывает сообщения из input-queue
@broker.subscriber("input-queue")
async def handle_message(msg: str, logger: Logger) -> None:
    logger.info(f"Получено сообщение: {msg}")
    # Отправляем результат в output-queue и final-queue
    processed_msg = f"Обработано: {msg.upper()}"
    await broker.publish(processed_msg, queue="output-queue")
    await broker.publish(processed_msg, queue="final-queue")


# Второй подписчик: обрабатывает сообщения из output-queue
@broker.subscriber("output-queue")
async def check_result(msg: str, logger: Logger) -> None:
    logger.info(f"Промежуточный результат: {msg}")
