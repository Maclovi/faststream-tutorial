# Объявление брокеров

FastStream предоставляет удобный способ объявления брокеров сообщений. Это основной компонент, через который происходит подписка на очереди и публикация сообщений.

---

## 🧱 Что такое брокер?

Брокер — это объект, представляющий подключение к системе обмена сообщениями, такой как RabbitMQ, Kafka, NATS или Redis.

FastStream предоставляет специализированные классы брокеров:

- `RabbitBroker` для RabbitMQ
- `KafkaBroker` для Kafka
- `NatsBroker` для NATS
- `RedisBroker` для Redis Pub/Sub

---

## ✍️ Пример с RabbitMQ

```python
from faststream.rabbit import RabbitBroker

broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
```

Здесь создаётся подключение к RabbitMQ через стандартный AMQP URI.

---

## 🔌 Подключение и отключение

FastStream сам управляет подключением и отключением брокера при запуске приложения через `broker.run()`.

Если вы работаете в тестах или в асинхронном окружении, можно управлять подключением вручную:

```python
await broker.connect()
# ... работа ...
await broker.close()
```

---

## 📦 Параметры подключения

Каждый тип брокера принимает уникальные параметры и URI. Например, Kafka:

```python
from faststream.kafka import KafkaBroker

broker = KafkaBroker("localhost:9092")
```

---

## 🧪 Резюме

- Брокер — это центральный объект FastStream-приложения.
- Вы используете его для подключения, подписки и публикации.
- FastStream поддерживает несколько популярных брокеров: RabbitMQ, Kafka, Redis и NATS.