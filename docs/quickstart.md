# Быстрый старт

В этом разделе вы быстро создадите минимальное FastStream-приложение с использованием RabbitMQ.

---

## 📦 Установка

Установите FastStream с зависимостями для RabbitMQ:

```bash
pip install faststream[rabbit]
```

## 🧪 Минимальный пример

```python
from faststream.rabbit import RabbitBroker

broker = RabbitBroker("amqp://guest:guest@localhost:5672/")

@broker.subscriber("my-queue")
async def handle(msg: str):
    print(f"Получено сообщение: {msg}")

if __name__ == "__main__":
    broker.run()
```

### 🔍 Что здесь происходит?

- RabbitBroker создаёт подключение к RabbitMQ.
- Декоратор @broker.subscriber(...) регистрирует функцию как хендлер на очередь my-queue.
- broker.run() запускает приложение и начинает слушать сообщения.

## ✅ Отправка сообщений (в другом скрипте)

```python
from faststream.rabbit import RabbitBroker

broker = RabbitBroker("amqp://guest:guest@localhost:5672/")

async def main():
    await broker.connect()
    await broker.publish("Привет!", "my-queue")

import asyncio
asyncio.run(main())
```

## 🎉 Вывод

FastStream позволяет начать работу с брокерами сообщений всего за несколько строк кода. Далее вы узнаете, как структурировать приложение, валидировать сообщения, использовать зависимости и интеграции.
